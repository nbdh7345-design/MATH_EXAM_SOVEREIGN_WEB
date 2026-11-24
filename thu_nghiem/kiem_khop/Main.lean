-- Thử nghiệm rủi ro 3 (M0): bản thô của tiện ích kiem_khop (mục 12.7).
-- Nạp module từ .olean, so kiểu định lý với kiểu dựng trực tiếp bằng Expr bằng kernel,
-- thu tập axiom bằng API. Không phân tích văn bản Lean nào của module được nạp.
import Lean
open Lean

/-- Kiểu mong đợi, dựng thẳng bằng Expr: `Eq Nat (Nat.add 2 2) 4`. -/
def kieuMongDoi : Expr :=
  mkApp3 (mkConst ``Eq [Level.one]) (mkConst ``Nat)
    (mkApp2 (mkConst ``Nat.add) (mkRawNatLit 2) (mkRawNatLit 2)) (mkRawNatLit 4)

def axiomChuan : List Name := [``propext, ``Classical.choice, ``Quot.sound]

def main (args : List String) : IO UInt32 := do
  let modName := args[0]!.toName
  initSearchPath (← findSysroot)
  -- Không bật initializer; không nạp phần mở rộng môi trường.
  let env ← importModules #[{ module := modName }] {} (loadExts := false)
  for ten in args.drop 1 do
    let n := ten.toName
    match env.find? n with
    | none => IO.println s!"{ten}: KHONG_TON_TAI"
    | some ci =>
      let laTheorem := match ci with | .thmInfo _ => true | _ => false
      let khop := match Kernel.isDefEq env {} ci.type kieuMongDoi with
        | .ok b => toString b
        | .error _ => "loi_kernel"
      let (axArr, _) ← (collectAxioms n : CoreM (Array Name)).toIO
        { fileName := "<kiem_khop>", fileMap := default } { env := env }
      let axs := axArr.toList
      let axOk := axs.all (axiomChuan.contains ·)
      IO.println s!"{ten}: theorem={laTheorem} khop_kieu={khop} axioms={axs} axiom_chuan={axOk}"
  return 0
