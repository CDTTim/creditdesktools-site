// Hand-checked test cases for every calculator. Run: node tools/test_calcs.js
// Expected values were worked out by hand or with an independent Python
// implementation, not by running calc.js. Add 3 cases for every new calculator.
const { calcs: C } = require("../public/assets/calc.js");
let fails = 0, passes = 0;
function near(name, got, want, tol = 0.01) {
  if (Math.abs(got - want) <= tol) { passes++; return; }
  fails++; console.log(`FAIL ${name}: got ${got}, want ${want}`);
}
function errs(name, out) { if (out.error) { passes++; } else { fails++; console.log(`FAIL ${name}: expected an error`); } }

// 1. Business loan: $100,000 at 8% for 5 years -> $2,027.64/mo (standard amortization table value)
let o = C["business-loan-calculator"]({ amount: 100000, rate: 8, years: 5 });
near("loan payment", o._raw.payment, 2027.64);
near("loan interest", o._raw.totalInterest, 21658.38, 0.05);
o = C["business-loan-calculator"]({ amount: 12000, rate: 0, years: 1 });
near("loan 0% payment", o._raw.payment, 1000);
errs("loan zero amount", C["business-loan-calculator"]({ amount: 0, rate: 5, years: 5 }));

// 2. DSCR: NOI 150k, existing 40k, new 250k at 8% / 10y -> annual 36,398.28, DSCR 1.9634; max loan at 1.25x = 549,476.54
o = C["dscr-calculator"]({ noi: 150000, existing: 40000, loan: 250000, rate: 8, years: 10, target: 1.25 });
near("dscr new annual", o._raw.newAnnual, 36398.28, 0.05);
near("dscr ratio", o._raw.dscr, 1.9634, 0.0001);
near("dscr max loan", o._raw.maxLoan, 549476.54, 0.5);
o = C["dscr-calculator"]({ noi: 100000, existing: 100000, loan: 0, rate: 0, years: 0, target: 1.25 });
near("dscr 1.00", o._raw.dscr, 1.0, 0.0001);

// 3. SBA 7(a): 500k at 10.5% / 10y -> 6,746.75; with 3% financed fee -> 6,949.15
o = C["sba-7a-loan-calculator"]({ amount: 500000, rate: 10.5, years: 10, feePct: 0 });
near("sba payment", o._raw.payment, 6746.75, 0.05);
o = C["sba-7a-loan-calculator"]({ amount: 500000, rate: 10.5, years: 10, feePct: 3 });
near("sba fee", o._raw.fee, 15000);
near("sba payment w fee", o._raw.payment, 6949.15, 0.05);

// 4. Factoring: 10,000 invoice, 80% advance, 3% per 30 days, paid in 45 days -> 2 periods, fee 600, rebate 1,400, APR 60.83%
o = C["invoice-factoring-cost-calculator"]({ invoice: 10000, advance: 80, fee: 3, period: 30, days: 45 });
near("fact fee", o._raw.fee, 600); near("fact rebate", o._raw.rebate, 1400); near("fact apr", o._raw.apr, 0.6083, 0.0001);
o = C["invoice-factoring-cost-calculator"]({ invoice: 50000, advance: 90, fee: 1.5, period: 10, days: 30 });
near("fact 10-day periods fee", o._raw.fee, 2250);

// 5. PO financing: 100k supplier, 100% funded, 3%/30 days, 75 days -> 3 periods, cost 9,000; sale 140k, other 5k -> profit 26,000, APR 43.8%
o = C["po-financing-cost-calculator"]({ supplier: 100000, funding: 100, fee: 3, days: 75, sale: 140000, other: 5000 });
near("po cost", o._raw.cost, 9000); near("po after", o._raw.after, 26000); near("po apr", o._raw.apr, 0.438, 0.0001);
o = C["po-financing-cost-calculator"]({ supplier: 80000, funding: 50, fee: 2, days: 30, sale: 100000, other: 0 });
near("po half funded", o._raw.cost, 800);

// 6. MCA: 50k funded, 1.35 factor, $1,500 fee, $535.71 daily -> ~126 payments, APR 139.54% (independent Python bisection)
o = C["mca-apr-calculator"]({ funded: 50000, factor: 1.35, fees: 1500, payment: 535.71, freq: 252 });
near("mca payback", o._raw.payback, 67500); near("mca n", o._raw.n, 126.001, 0.01); near("mca apr", o._raw.apr, 1.3954, 0.001);
errs("mca factor below 1", C["mca-apr-calculator"]({ funded: 50000, factor: 0.9, fees: 0, payment: 500, freq: 252 }));

// 7. Cash conversion cycle: rev 1.2M, COGS 800k, inv 100k, AR 150k, AP 80k -> DIO 45.625, DSO 45.625, DPO 36.5, CCC 54.75
o = C["cash-conversion-cycle-calculator"]({ revenue: 1200000, cogs: 800000, inventory: 100000, ar: 150000, ap: 80000 });
near("ccc dio", o._raw.dio, 45.625); near("ccc dpo", o._raw.dpo, 36.5); near("ccc", o._raw.ccc, 54.75);

// 8. Break-even: fixed 20k, price 50, variable 30 -> 1,000 units, $50,000
o = C["break-even-calculator"]({ fixed: 20000, price: 50, variable: 30, target: 0 });
near("be units", o._raw.units, 1000); near("be revenue", o._raw.revenue, 50000);
errs("be negative margin", C["break-even-calculator"]({ fixed: 1000, price: 10, variable: 12 }));

// 9. Borrowing base: AR 500k - 40k over 90 - 10k other = 450k x 85% = 382.5k; inventory (300k-50k) x 50% = 125k capped at 100k; base 482.5k; loan 400k -> 82.5k available
o = C["borrowing-base-calculator"]({ ar: 500000, over90: 40000, arOther: 10000, arAdvance: 85, inventory: 300000, invIneligible: 50000, invAdvance: 50, invCap: 100000, loan: 400000 });
near("bb ar avail", o._raw.arAvail, 382500); near("bb inv capped", o._raw.invAvail, 100000);
near("bb base", o._raw.base, 482500); near("bb excess", o._raw.excess, 82500);

// 10. DSO: 150k AR / 1.2M sales x 365 = 45.625 days
o = C["dso-calculator"]({ ar: 150000, sales: 1200000, days: 365, terms: 30 });
near("dso", o._raw.dso, 45.625);
o = C["dso-calculator"]({ ar: 30000, sales: 90000, days: 90, terms: 0 });
near("dso quarter", o._raw.dso, 30);

// 11. Margin vs markup: cost 60, price 100 -> margin 40%, markup 66.67%; 50% target margin -> price 120
o = C["margin-markup-calculator"]({ cost: 60, price: 100, targetMargin: 50 });
near("margin", o._raw.margin, 0.4); near("markup", o._raw.markup, 0.6667, 0.0001); near("target price", o._raw.targetPrice, 120);

// 12. Current/quick: cash 50k, AR 100k, inv 150k, other 20k, CL 160k -> current 2.00, quick 0.9375, WC 160k
o = C["current-ratio-calculator"]({ cash: 50000, ar: 100000, inventory: 150000, otherCA: 20000, cl: 160000 });
near("current", o._raw.current, 2.0); near("quick", o._raw.quick, 0.9375, 0.0001); near("wc", o._raw.wc, 160000);

console.log(`${passes} passed, ${fails} failed`);
process.exit(fails ? 1 : 0);
