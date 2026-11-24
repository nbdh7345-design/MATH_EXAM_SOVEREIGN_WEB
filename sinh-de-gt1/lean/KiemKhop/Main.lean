-- TIN CẬY — tiện ích đối chiếu kiem_khop (mục 12.7).
-- Bản M0 (thử nghiệm rủi ro 3); hoàn thiện và duyệt ở M4.
--
-- Không phân tích hay elaborate văn bản Lean nào của module được nạp:
--   * nạp môi trường từ .olean; không bật initializer; không nạp phần mở rộng môi trường;
--   * kiểu mong đợi dựng thẳng bằng Expr từ S-biểu thức trong tệp yêu cầu;
--   * so kiểu bằng kernel; thu axiom bằng API.
--
-- Cách dùng: kiem_khop <yeu_cau.json> <ket_qua.json>
--   yeu_cau: {"module": "...", "dinh_ly": "...", "kieu": "<S-biểu thức>"}
-- S-biểu thức của Expr:
--   (c <Tên> <cấp>...)   hằng; cấp vũ trụ là số tự nhiên
--   (a <hàm> <đối>...)   áp dụng
--   (n <số>)             literal số tự nhiên
import Lean
open Lean

namespace KiemKhop

inductive SE where
  | atom (s : String)
  | list (xs : List SE)
  deriving Inhabited

/-- Tách token: "(", ")" và các chuỗi không chứa khoảng trắng hay ngoặc. -/
def tachToken (s : String) : List String := Id.run do
  let mut out : Array String := #[]
  let mut cur : String := ""
  for ch in s.toList do
    if ch == '(' || ch == ')' then
      if !cur.isEmpty then
        out := out.push cur
        cur := ""
      out := out.push (String.singleton ch)
    else if ch.isWhitespace then
      if !cur.isEmpty then
        out := out.push cur
        cur := ""
    else
      cur := cur.push ch
  if !cur.isEmpty then
    out := out.push cur
  return out.toList

mutual
  partial def docSE : List String → Except String (SE × List String)
    | "(" :: rest => docDanhSach rest #[]
    | ")" :: _ => throw "thừa dấu )"
    | t :: rest => pure (.atom t, rest)
    | [] => throw "S-biểu thức rỗng"

  partial def docDanhSach : List String → Array SE → Except String (SE × List String)
    | ")" :: rest, acc => pure (.list acc.toList, rest)
    | [], _ => throw "thiếu dấu )"
    | ts, acc => do
      let (e, rest) ← docSE ts
      docDanhSach rest (acc.push e)
end

partial def sangExpr : SE → Except String Expr
  | .list (.atom "c" :: .atom ten :: cap) => do
    let caps ← cap.mapM fun
      | .atom s => match s.toNat? with
        | some k => pure (Level.ofNat k)
        | none => throw s!"cấp vũ trụ không hợp lệ: {s}"
      | .list _ => throw "cấp vũ trụ không hợp lệ"
    pure (mkConst ten.toName caps)
  | .list [.atom "n", .atom k] =>
    match k.toNat? with
    | some v => pure (mkRawNatLit v)
    | none => throw s!"số tự nhiên không hợp lệ: {k}"
  | .list (.atom "a" :: f :: xs) => do
    let fe ← sangExpr f
    let xe ← xs.mapM sangExpr
    pure (mkAppN fe xe.toArray)
  | _ => throw "S-biểu thức không hợp lệ"

def axiomChuan : List Name := [``propext, ``Classical.choice, ``Quot.sound]

def kiem (env : Environment) (ten : Name) (kieu : Expr) : IO Json := do
  match env.find? ten with
  | none => return Json.mkObj [("ton_tai", toJson false)]
  | some ci =>
    let laTheorem := match ci with
      | .thmInfo _ => true
      | _ => false
    let (khop, loi) := match Kernel.isDefEq env {} ci.type kieu with
      | .ok b => (b, "")
      | .error _ => (false, "loi_kernel")
    let (axArr, _) ← (collectAxioms ten : CoreM (Array Name)).toIO
      { fileName := "<kiem_khop>", fileMap := default } { env := env }
    return Json.mkObj [
      ("ton_tai", toJson true),
      ("la_theorem", toJson laTheorem),
      ("khong_tham_so_vu_tru", toJson ci.levelParams.isEmpty),
      ("khop_kieu", toJson khop),
      ("loi", toJson loi),
      ("axioms", toJson (axArr.toList.map toString)),
      ("axiom_chuan", toJson (axArr.toList.all (axiomChuan.contains ·)))]

def chay (vao ra : String) : IO Unit := do
  let j ← IO.ofExcept (Json.parse (← IO.FS.readFile vao))
  let modTen ← IO.ofExcept (j.getObjValAs? String "module")
  let dinhLy ← IO.ofExcept (j.getObjValAs? String "dinh_ly")
  let kieuChuoi ← IO.ofExcept (j.getObjValAs? String "kieu")
  let (se, du) ← IO.ofExcept (docSE (tachToken kieuChuoi))
  unless du.isEmpty do
    throw (IO.userError "thừa token sau S-biểu thức")
  let kieu ← IO.ofExcept (sangExpr se)
  initSearchPath (← findSysroot)
  -- Không gọi enableInitializersExecution; không nạp phần mở rộng môi trường.
  let env ← importModules #[{ module := modTen.toName }] {} (loadExts := false)
  let kq ← kiem env dinhLy.toName kieu
  IO.FS.writeFile ra kq.compress

end KiemKhop

def main (args : List String) : IO UInt32 := do
  match args with
  | [vao, ra] =>
    try
      KiemKhop.chay vao ra
      return 0
    catch e =>
      IO.eprintln s!"kiem_khop: {e}"
      return 1
  | _ =>
    IO.eprintln "cách dùng: kiem_khop <yeu_cau.json> <ket_qua.json>"
    return 2
