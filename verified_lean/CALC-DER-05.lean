-- Lean 4 Core verification for CALC-DER-05 (Leibniz: (x e^{mx})'' = 2 * m e^{mx} + x * m^2 e^{mx})
def secondDerivAt0 (m : Nat) : Nat := 2 * 1 * m + 0 * m ^ 2
def options (m : Nat) : List Nat := [3 * m, 2 * m, m, m ^ 2 + 2 * m]

theorem calc_der_05_answer :
    (List.range 8).all (fun k => let m := k + 2; secondDerivAt0 m == 2 * m) = true := by decide
theorem calc_der_05_distinct :
    (List.range 8).all (fun k => let m := k + 2; (options m).Nodup) = true := by decide
