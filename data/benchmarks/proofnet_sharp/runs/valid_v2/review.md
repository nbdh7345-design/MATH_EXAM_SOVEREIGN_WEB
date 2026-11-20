# Các mệnh đề cần chấm tay

Ghi kết luận vào manual.json, ví dụ: {"Rudin|exercise_5_1": {"top": true, "confirmed": true}}

## Pugh|exercise_3_4 · top

**Chấm tự động:** không c/m được

**Đề:** Prove that $\sqrt{n+1}-\sqrt{n} \rightarrow 0$ as $n \rightarrow \infty$.

**Tham chiếu:**
```lean
theorem exercise_3_4 (n : ℕ) :
  Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) :=
```

**Mệnh đề sinh ra:**
```lean
Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 0)
```

**Bản diễn đạt lại:** Chứng minh rằng dãy số thực xác định bởi u_n = √(n + 1) − √n (với n là số tự nhiên) có giới hạn bằng 0 khi n tiến tới +∞.

## Pugh|exercise_3_4 · confirmed

**Chấm tự động:** không c/m được

**Đề:** Prove that $\sqrt{n+1}-\sqrt{n} \rightarrow 0$ as $n \rightarrow \infty$.

**Tham chiếu:**
```lean
theorem exercise_3_4 (n : ℕ) :
  Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) :=
```

**Mệnh đề sinh ra:**
```lean
Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 0)
```

**Bản diễn đạt lại:** Chứng minh rằng dãy số thực xác định bởi u_n = √(n + 1) − √n (với n là số tự nhiên) có giới hạn bằng 0 khi n tiến tới +∞.

## Rudin|exercise_3_3 · top

**Chấm tự động:** không c/m được

**Đề:** If $s_{1}=\sqrt{2}$, and $s_{n+1}=\sqrt{2+\sqrt{s_{n}}} \quad(n=1,2,3, \ldots),$ prove that $\left\{s_{n}\right\}$ converges, and that $s_{n}<2$ for $n=1,2,3, \ldots$.

**Tham chiếu:**
```lean
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

theorem exercise_3_3
  : ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 :=
```

**Mệnh đề sinh ra:**
```lean
∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ (∀ n : ℕ, 1 ≤ n → s n < 2)
```

**Bản diễn đạt lại:** Cho dãy số thực $(s_n)_{n \in \mathbb{N}}$, trong đó $s_0$ không có ràng buộc nào. Giả sử $s_1 = \sqrt{2}$ và $s_{n+1} = \sqrt{2 + \sqrt{s_n}}$ với mọi $n \geq 1$. Chứng minh rằng:
a) Dãy $(s_n)$ hội tụ, tức tồn tại số thực $L$ sao cho $\lim_{n \to +\infty} s_n = L$;
b) $s_n < 2$ với mọi $n \geq 1$.

## Rudin|exercise_3_3 · confirmed

**Chấm tự động:** không c/m được

**Đề:** If $s_{1}=\sqrt{2}$, and $s_{n+1}=\sqrt{2+\sqrt{s_{n}}} \quad(n=1,2,3, \ldots),$ prove that $\left\{s_{n}\right\}$ converges, and that $s_{n}<2$ for $n=1,2,3, \ldots$.

**Tham chiếu:**
```lean
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

theorem exercise_3_3
  : ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 :=
```

**Mệnh đề sinh ra:**
```lean
∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ (∀ n : ℕ, 1 ≤ n → s n < 2)
```

**Bản diễn đạt lại:** Cho dãy số thực $(s_n)_{n \in \mathbb{N}}$, trong đó $s_0$ không có ràng buộc nào. Giả sử $s_1 = \sqrt{2}$ và $s_{n+1} = \sqrt{2 + \sqrt{s_n}}$ với mọi $n \geq 1$. Chứng minh rằng:
a) Dãy $(s_n)$ hội tụ, tức tồn tại số thực $L$ sao cho $\lim_{n \to +\infty} s_n = L$;
b) $s_n < 2$ với mọi $n \geq 1$.

## Rudin|exercise_4_19 · top

**Chấm tự động:** không c/m được

**Đề:** Suppose $f$ is a real function with domain $R^{1}$ which has the intermediate value property: if $f(a)<c<f(b)$, then $f(x)=c$ for some $x$ between $a$ and $b$. Suppose also, for every rational $r$, that the set of all $x$ with $f(x)=r$ is closed. Prove that $f$ is continuous.

**Tham chiếu:**
```lean
theorem exercise_4_19
  {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}) : Continuous f :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ thỏa mãn hai điều kiện sau:
(i) Với mọi a, b, c ∈ ℝ, nếu f(a) < c < f(b) thì tồn tại x thuộc đoạn nối a và b (tức là x ∈ [min(a, b), max(a, b)]) sao cho f(x) = c.
(ii) Với mọi số hữu tỉ r ∈ ℚ, tập {x ∈ ℝ : f(x) = r} là tập đóng.
Chứng minh rằng f liên tục trên ℝ.

## Rudin|exercise_4_19 · confirmed

**Chấm tự động:** không c/m được

**Đề:** Suppose $f$ is a real function with domain $R^{1}$ which has the intermediate value property: if $f(a)<c<f(b)$, then $f(x)=c$ for some $x$ between $a$ and $b$. Suppose also, for every rational $r$, that the set of all $x$ with $f(x)=r$ is closed. Prove that $f$ is continuous.

**Tham chiếu:**
```lean
theorem exercise_4_19
  {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}) : Continuous f :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ thỏa mãn hai điều kiện sau:
(i) Với mọi a, b, c ∈ ℝ, nếu f(a) < c < f(b) thì tồn tại x thuộc đoạn nối a và b (tức là x ∈ [min(a, b), max(a, b)]) sao cho f(x) = c.
(ii) Với mọi số hữu tỉ r ∈ ℚ, tập {x ∈ ℝ : f(x) = r} là tập đóng.
Chứng minh rằng f liên tục trên ℝ.

## Rudin|exercise_4_24 · top

**Chấm tự động:** 1 chiều: sinh ⇒ chuẩn

**Đề:** Assume that $f$ is a continuous real function defined in $(a, b)$ such that $f\left(\frac{x+y}{2}\right) \leq \frac{f(x)+f(y)}{2}$ for all $x, y \in(a, b)$. Prove that $f$ is convex.

**Tham chiếu:**
```lean
theorem exercise_4_24 {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
  ConvexOn ℝ (Set.Ioo a b) f :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ và hai số thực a, b thỏa mãn a < b. Giả sử f liên tục trên khoảng (a, b) và với mọi x, y ∈ (a, b) ta có f((x + y)/2) ≤ (f(x) + f(y))/2. Chứng minh rằng f là hàm lồi trên khoảng (a, b).

## Rudin|exercise_4_24 · confirmed

**Chấm tự động:** 1 chiều: sinh ⇒ chuẩn

**Đề:** Assume that $f$ is a continuous real function defined in $(a, b)$ such that $f\left(\frac{x+y}{2}\right) \leq \frac{f(x)+f(y)}{2}$ for all $x, y \in(a, b)$. Prove that $f$ is convex.

**Tham chiếu:**
```lean
theorem exercise_4_24 {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
  ConvexOn ℝ (Set.Ioo a b) f :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ và hai số thực a, b thỏa mãn a < b. Giả sử f liên tục trên khoảng (a, b) và với mọi x, y ∈ (a, b) ta có f((x + y)/2) ≤ (f(x) + f(y))/2. Chứng minh rằng f là hàm lồi trên khoảng (a, b).

## Rudin|exercise_5_2 · top

**Chấm tự động:** không c/m được

**Đề:** Suppose $f^{\prime}(x)>0$ in $(a, b)$. Prove that $f$ is strictly increasing in $(a, b)$, and let $g$ be its inverse function. Prove that $g$ is differentiable, and that $g^{\prime}(f(x))=\frac{1}{f^{\prime}(x)} \quad(a<x<b)$.

**Tham chiếu:**
```lean
theorem exercise_5_2 {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹) :
  StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x :=
```

**Mệnh đề sinh ra:**
```lean
∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x
```

**Bản diễn đạt lại:** Cho a, b là các số thực với a < b. Cho f: ℝ → ℝ và g: ℝ → ℝ thỏa mãn:
(i) Với mọi x ∈ (a, b), hàm f khả vi tại x và f'(x) > 0.
(ii) Với mọi x ∈ (a, b), g(f(x)) = x.
(iii) Với mọi y ∈ f((a, b)), f(g(y)) = y.
Chứng minh rằng:
(1) f đồng biến ngặt trên khoảng (a, b);
(2) Với mọi x ∈ (a, b), hàm g khả vi tại f(x) và g'(f(x)) = 1 / f'(x).

## Rudin|exercise_5_4 · top

**Chấm tự động:** không c/m được

**Đề:** If $C_{0}+\frac{C_{1}}{2}+\cdots+\frac{C_{n-1}}{n}+\frac{C_{n}}{n+1}=0,$ where $C_{0}, \ldots, C_{n}$ are real constants, prove that the equation $C_{0}+C_{1} x+\cdots+C_{n-1} x^{n-1}+C_{n} x^{n}=0$ has at least one real root between 0 and 1.

**Tham chiếu:**
```lean
theorem exercise_5_4 {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i in (range (n + 1)), (C i) / (i + 1) = 0) :
  ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i in range (n + 1), (C i) * (x^i) = 0 :=
```

**Mệnh đề sinh ra:**
```lean
∀ (C : ℕ → ℝ) (n : ℕ), (∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0) → ∃ x : ℝ, x ∈ Set.Ioo (0:ℝ) 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0
```

**Bản diễn đạt lại:** Cho dãy số thực (C_k)_{k∈ℕ} và số tự nhiên n. Giả sử Σ_{k=0}^{n} C_k/(k+1) = 0. Chứng minh rằng tồn tại số thực x thuộc khoảng (0, 1) sao cho Σ_{k=0}^{n} C_k·x^k = 0.

## Rudin|exercise_5_4 · confirmed

**Chấm tự động:** không c/m được

**Đề:** If $C_{0}+\frac{C_{1}}{2}+\cdots+\frac{C_{n-1}}{n}+\frac{C_{n}}{n+1}=0,$ where $C_{0}, \ldots, C_{n}$ are real constants, prove that the equation $C_{0}+C_{1} x+\cdots+C_{n-1} x^{n-1}+C_{n} x^{n}=0$ has at least one real root between 0 and 1.

**Tham chiếu:**
```lean
theorem exercise_5_4 {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i in (range (n + 1)), (C i) / (i + 1) = 0) :
  ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i in range (n + 1), (C i) * (x^i) = 0 :=
```

**Mệnh đề sinh ra:**
```lean
∀ (C : ℕ → ℝ) (n : ℕ), (∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0) → ∃ x : ℝ, x ∈ Set.Ioo (0:ℝ) 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0
```

**Bản diễn đạt lại:** Cho dãy số thực (C_k)_{k∈ℕ} và số tự nhiên n. Giả sử Σ_{k=0}^{n} C_k/(k+1) = 0. Chứng minh rằng tồn tại số thực x thuộc khoảng (0, 1) sao cho Σ_{k=0}^{n} C_k·x^k = 0.

## Rudin|exercise_5_6 · top

**Chấm tự động:** không c/m được

**Đề:** Suppose (a) $f$ is continuous for $x \geq 0$, (b) $f^{\prime}(x)$ exists for $x>0$, (c) $f(0)=0$, (d) $f^{\prime}$ is monotonically increasing. Put $g(x)=\frac{f(x)}{x} \quad(x>0)$ and prove that $g$ is monotonically increasing.

**Tham chiếu:**
```lean
theorem exercise_5_6
  {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
  MonotoneOn (λ x => f x / x) (Set.Ioi 0) :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x : ℝ, 0 < x → DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0)
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ thỏa mãn các điều kiện sau:
(i) f liên tục trên đoạn [0, +∞);
(ii) với mọi x > 0, f có đạo hàm tại x;
(iii) f(0) = 0;
(iv) hàm đạo hàm f' không giảm trên khoảng (0, +∞).
Chứng minh rằng hàm số g(x) = f(x)/x không giảm trên khoảng (0, +∞).

## Rudin|exercise_5_6 · confirmed

**Chấm tự động:** không c/m được

**Đề:** Suppose (a) $f$ is continuous for $x \geq 0$, (b) $f^{\prime}(x)$ exists for $x>0$, (c) $f(0)=0$, (d) $f^{\prime}$ is monotonically increasing. Put $g(x)=\frac{f(x)}{x} \quad(x>0)$ and prove that $g$ is monotonically increasing.

**Tham chiếu:**
```lean
theorem exercise_5_6
  {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
  MonotoneOn (λ x => f x / x) (Set.Ioi 0) :=
```

**Mệnh đề sinh ra:**
```lean
∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x : ℝ, 0 < x → DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0)
```

**Bản diễn đạt lại:** Cho hàm số f: ℝ → ℝ thỏa mãn các điều kiện sau:
(i) f liên tục trên đoạn [0, +∞);
(ii) với mọi x > 0, f có đạo hàm tại x;
(iii) f(0) = 0;
(iv) hàm đạo hàm f' không giảm trên khoảng (0, +∞).
Chứng minh rằng hàm số g(x) = f(x)/x không giảm trên khoảng (0, +∞).

## Rudin|exercise_5_15 · top

**Chấm tự động:** không c/m được

**Đề:** Suppose $a \in R^{1}, f$ is a twice-differentiable real function on $(a, \infty)$, and $M_{0}, M_{1}, M_{2}$ are the least upper bounds of $|f(x)|,\left|f^{\prime}(x)\right|,\left|f^{\prime \prime}(x)\right|$, respectively, on $(a, \infty)$. Prove that $M_{1}^{2} \leq 4 M_{0} M_{2} .$

**Tham chiếu:**
```lean
theorem exercise_5_15 {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
  (M1 ^ 2) ≤ 4 * M0 * M2 :=
```

**Mệnh đề sinh ra:**
```lean
∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |f x|} M0 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2
```

**Bản diễn đạt lại:** Cho các số thực a, M0, M1, M2 và hàm số thực f : ℝ → ℝ. Giả sử với mọi số thực x > a, f khả vi tại x và hàm đạo hàm f' cũng khả vi tại x. Đặt M0 là cận trên đúng của tập {|f(x)| : x > a}, M1 là cận trên đúng của tập {|f'(x)| : x > a}, và M2 là cận trên đúng của tập {|f''(x)| : x > a}. Chứng minh rằng M1² ≤ 4·M0·M2.

## Rudin|exercise_5_15 · confirmed

**Chấm tự động:** không c/m được

**Đề:** Suppose $a \in R^{1}, f$ is a twice-differentiable real function on $(a, \infty)$, and $M_{0}, M_{1}, M_{2}$ are the least upper bounds of $|f(x)|,\left|f^{\prime}(x)\right|,\left|f^{\prime \prime}(x)\right|$, respectively, on $(a, \infty)$. Prove that $M_{1}^{2} \leq 4 M_{0} M_{2} .$

**Tham chiếu:**
```lean
theorem exercise_5_15 {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
  (M1 ^ 2) ≤ 4 * M0 * M2 :=
```

**Mệnh đề sinh ra:**
```lean
∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |f x|} M0 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2
```

**Bản diễn đạt lại:** Cho các số thực a, M0, M1, M2 và hàm số thực f : ℝ → ℝ. Giả sử với mọi số thực x > a, f khả vi tại x và hàm đạo hàm f' cũng khả vi tại x. Đặt M0 là cận trên đúng của tập {|f(x)| : x > a}, M1 là cận trên đúng của tập {|f'(x)| : x > a}, và M2 là cận trên đúng của tập {|f''(x)| : x > a}. Chứng minh rằng M1² ≤ 4·M0·M2.

## Pugh|exercise_2_12a · top

**Chấm tự động:** không c/m được

**Đề:** Let $(p_n)$ be a sequence and $f:\mathbb{N}\to\mathbb{N}$. The sequence $(q_k)_{k\in\mathbb{N}}$ with $q_k=p_{f(k)}$ is called a rearrangement of $(p_n)$. Show that if $f$ is an injection, the limit of a sequence is unaffected by rearrangement.

**Tham chiếu:**
```lean
theorem exercise_2_12a {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)) :
  Tendsto (λ n => p (f n)) atTop (𝓝 a) :=
```

**Mệnh đề sinh ra:**
```lean
∀ (p : ℕ → ℝ) (f : ℕ → ℕ), Function.Injective f → ∀ L : ℝ, Filter.Tendsto p Filter.atTop (nhds L) → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop (nhds L)
```

**Bản diễn đạt lại:** Cho dãy số thực $(p_n)_{n\in\mathbb{N}}$, tức là $p:\mathbb{N}\to\mathbb{R}$, và ánh xạ $f:\mathbb{N}\to\mathbb{N}$ là đơn ánh. Với mọi số thực $L$, nếu $\lim_{n\to+\infty} p_n = L$ thì $\lim_{k\to+\infty} p_{f(k)} = L$.

## Rudin|exercise_1_5 · top

**Chấm tự động:** 1 chiều: sinh ⇒ chuẩn

**Đề:** Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.

**Tham chiếu:**
```lean
theorem exercise_1_5 (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}) :
  sInf A = - sSup minus_A :=
```

**Mệnh đề sinh ra:**
```lean
∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ i s : ℝ, IsGLB A i ∧ IsLUB ((fun x : ℝ => -x) '' A) s ∧ i = -s
```

**Bản diễn đạt lại:** Cho A là một tập con tùy ý của tập số thực ℝ. Giả sử A khác rỗng và A bị chặn dưới. Chứng minh rằng tồn tại các số thực i và s sao cho: i là cận dưới lớn nhất của A (infimum của A), s là cận trên nhỏ nhất của tập {-x : x ∈ A}, và i = -s.

## Rudin|exercise_1_5 · confirmed

**Chấm tự động:** 1 chiều: sinh ⇒ chuẩn

**Đề:** Let $A$ be a nonempty set of real numbers which is bounded below. Let $-A$ be the set of all numbers $-x$, where $x \in A$. Prove that $\inf A=-\sup (-A)$.

**Tham chiếu:**
```lean
theorem exercise_1_5 (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}) :
  sInf A = - sSup minus_A :=
```

**Mệnh đề sinh ra:**
```lean
∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ i s : ℝ, IsGLB A i ∧ IsLUB ((fun x : ℝ => -x) '' A) s ∧ i = -s
```

**Bản diễn đạt lại:** Cho A là một tập con tùy ý của tập số thực ℝ. Giả sử A khác rỗng và A bị chặn dưới. Chứng minh rằng tồn tại các số thực i và s sao cho: i là cận dưới lớn nhất của A (infimum của A), s là cận trên nhỏ nhất của tập {-x : x ∈ A}, và i = -s.

## Rudin|exercise_4_8b · top

**Chấm tự động:** không c/m được

**Đề:** Let $E$ be a bounded set in $R^{1}$. Prove that there exists a real function $f$ such that $f$ is uniformly continuous and is not bounded on $E$.

**Tham chiếu:**
```lean
theorem exercise_4_8b
  (E : Set ℝ) (h : Bornology.IsBounded E) :
  ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) :=
```

**Mệnh đề sinh ra:**
```lean
∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M
```

**Bản diễn đạt lại:** Chứng minh rằng: với mọi tập hợp E ⊆ ℝ bị chặn, tồn tại hàm số f: ℝ → ℝ liên tục đều trên ℝ sao cho không tồn tại số thực M nào thỏa mãn |f(x)| ≤ M với mọi x ∈ E.
