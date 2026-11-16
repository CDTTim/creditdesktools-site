/* Credit Desk Tools calculator engine.
   Every calculator is a pure function: inputs object in, results object out.
   The same file runs in the browser and in Node (tools/test_calcs.js). */
(function (root) {
  "use strict";

  // ---------- helpers ----------
  function pmt(principal, annualRatePct, months) {
    var r = annualRatePct / 100 / 12;
    if (months <= 0) return 0;
    if (r === 0) return principal / months;
    return (principal * r) / (1 - Math.pow(1 + r, -months));
  }
  function pv(payment, annualRatePct, months) {
    var r = annualRatePct / 100 / 12;
    if (r === 0) return payment * months;
    return (payment * (1 - Math.pow(1 + r, -months))) / r;
  }
  function usd(x, dp) {
    if (!isFinite(x)) return "—";
    var d = dp === undefined ? 2 : dp;
    var s = Math.abs(x).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
    return (x < 0 ? "-$" : "$") + s;
  }
  function pct(x, dp) {
    if (!isFinite(x)) return "—";
    return (x * 100).toFixed(dp === undefined ? 1 : dp) + "%";
  }
  function num(x, dp) {
    if (!isFinite(x)) return "—";
    return x.toLocaleString("en-US", { minimumFractionDigits: dp || 0, maximumFractionDigits: dp || 0 });
  }
  function need(v, keys) {
    for (var i = 0; i < keys.length; i++) {
      var x = v[keys[i]];
      if (x === null || x === undefined || isNaN(x)) return "Enter a value for every required field.";
    }
    return null;
  }

  // ---------- calculators ----------
  var C = {};

  // 1. Business loan payment + yearly amortization
  C["business-loan-calculator"] = function (v) {
    var e = need(v, ["amount", "rate", "years"]); if (e) return { error: e };
    if (v.amount <= 0 || v.years <= 0 || v.rate < 0) return { error: "Amount and term must be above zero." };
    var n = Math.round(v.years * 12), p = pmt(v.amount, v.rate, n), r = v.rate / 1200;
    var bal = v.amount, rows = [], yI = 0, yP = 0, y1I = 0;
    for (var m = 1; m <= n; m++) {
      var i = bal * r, pr = p - i; bal -= pr; yI += i; yP += pr;
      if (m === 12 || (n < 12 && m === n)) y1I = yI;
      if (m % 12 === 0 || m === n) {
        rows.push([Math.ceil(m / 12), usd(yP), usd(yI), usd(Math.max(bal, 0))]);
        yI = 0; yP = 0;
      }
    }
    var total = p * n;
    return {
      payment: usd(p), totalInterest: usd(total - v.amount), totalPaid: usd(total), year1Interest: usd(y1I),
      _table: { head: ["Year", "Principal paid", "Interest paid", "Ending balance"], rows: rows },
      _raw: { payment: p, totalInterest: total - v.amount }
    };
  };

  // 2. DSCR with optional new loan and max supportable loan
  C["dscr-calculator"] = function (v) {
    var e = need(v, ["noi", "existing", "target"]); if (e) return { error: e };
    var n = Math.round((v.years || 0) * 12);
    var newAnnual = v.loan > 0 && n > 0 ? pmt(v.loan, v.rate || 0, n) * 12 : 0;
    var debt = v.existing + newAnnual;
    var dscr = debt > 0 ? v.noi / debt : Infinity;
    var room = v.noi / v.target - v.existing;
    var maxLoan = room > 0 && n > 0 ? pv(room / 12, v.rate || 0, n) : 0;
    var verdict = !isFinite(dscr) ? "No debt service entered."
      : dscr >= v.target ? "Meets your " + v.target.toFixed(2) + "x target."
      : dscr >= 1 ? "Covers debt, but below your " + v.target.toFixed(2) + "x target."
      : "Cash flow does not cover debt service.";
    return {
      newDebt: usd(newAnnual), totalDebt: usd(debt),
      dscr: isFinite(dscr) ? dscr.toFixed(2) + "x" : "—", verdict: verdict,
      maxLoan: n > 0 ? usd(maxLoan, 0) : "Enter a rate and term",
      _raw: { dscr: dscr, newAnnual: newAnnual, maxLoan: maxLoan }
    };
  };

  // 3. SBA 7(a) payment with optional financed guarantee fee
  C["sba-7a-loan-calculator"] = function (v) {
    var e = need(v, ["amount", "rate", "years"]); if (e) return { error: e };
    if (v.amount <= 0 || v.years <= 0) return { error: "Amount and term must be above zero." };
    var fee = v.amount * (v.feePct || 0) / 100, principal = v.amount + fee, n = Math.round(v.years * 12);
    var p = pmt(principal, v.rate, n), total = p * n;
    return {
      fee: usd(fee), principal: usd(principal), payment: usd(p),
      totalInterest: usd(total - principal), totalPaid: usd(total),
      _raw: { payment: p, fee: fee }
    };
  };

  // 4. Invoice factoring true cost
  C["invoice-factoring-cost-calculator"] = function (v) {
    var e = need(v, ["invoice", "advance", "fee", "period", "days"]); if (e) return { error: e };
    if (v.invoice <= 0 || v.days <= 0 || v.period <= 0) return { error: "Invoice, days and fee period must be above zero." };
    var periods = Math.ceil(v.days / v.period), fee = v.invoice * v.fee / 100 * periods;
    var adv = v.invoice * v.advance / 100, rebate = v.invoice - adv - fee;
    var apr = adv > 0 ? (fee / adv) * (365 / v.days) : Infinity;
    return {
      advanceAmt: usd(adv), feeAmt: usd(fee), periods: num(periods), rebate: usd(rebate), apr: pct(apr),
      _raw: { fee: fee, adv: adv, rebate: rebate, apr: apr }
    };
  };

  // 5. Purchase order financing cost and margin impact
  C["po-financing-cost-calculator"] = function (v) {
    var e = need(v, ["supplier", "funding", "fee", "days", "sale"]); if (e) return { error: e };
    if (v.supplier <= 0 || v.days <= 0 || v.sale <= 0) return { error: "Supplier cost, sale price and days must be above zero." };
    var funded = v.supplier * v.funding / 100, periods = Math.ceil(v.days / 30);
    var cost = funded * v.fee / 100 * periods, other = v.other || 0;
    var before = v.sale - v.supplier - other, after = before - cost;
    var apr = funded > 0 ? (cost / funded) * (365 / v.days) : Infinity;
    return {
      funded: usd(funded), cost: usd(cost), before: usd(before), after: usd(after),
      margin: pct(after / v.sale), share: before > 0 ? pct(cost / before) : "—", apr: pct(apr),
      _raw: { cost: cost, after: after, apr: apr }
    };
  };

  // 6. Merchant cash advance true APR (solves the implied periodic rate)
  C["mca-apr-calculator"] = function (v) {
    var e = need(v, ["funded", "factor", "payment", "freq"]); if (e) return { error: e };
    if (v.funded <= 0 || v.factor < 1 || v.payment <= 0) return { error: "Funded amount and payment must be above zero, and the factor rate at least 1.00." };
    var ppy = v.freq === 52 ? 52 : 252;
    var payback = v.funded * v.factor, net = v.funded - (v.fees || 0), n = payback / v.payment;
    if (net <= 0) return { error: "Fees can't exceed the funded amount." };
    function f(r) { return v.payment * (1 - Math.pow(1 + r, -n)) / r - net; }
    var lo = 1e-9, hi = 1, r = 0;
    if (payback <= net) r = 0; else {
      for (var k = 0; k < 200; k++) { r = (lo + hi) / 2; if (f(r) > 0) lo = r; else hi = r; }
    }
    var apr = r * ppy;
    return {
      payback: usd(payback), cost: usd(payback - net), count: num(Math.ceil(n)),
      term: (n / ppy * 12).toFixed(1) + " months", apr: pct(apr),
      _raw: { apr: apr, n: n, payback: payback }
    };
  };

  // 7. Cash conversion cycle
  C["cash-conversion-cycle-calculator"] = function (v) {
    var e = need(v, ["revenue", "cogs", "inventory", "ar", "ap"]); if (e) return { error: e };
    if (v.revenue <= 0 || v.cogs <= 0) return { error: "Revenue and cost of goods sold must be above zero." };
    var dio = v.inventory / v.cogs * 365, dso = v.ar / v.revenue * 365, dpo = v.ap / v.cogs * 365;
    var ccc = dio + dso - dpo, cashPerDay = v.cogs / 365;
    return {
      dio: num(dio, 1) + " days", dso: num(dso, 1) + " days", dpo: num(dpo, 1) + " days",
      ccc: num(ccc, 1) + " days", tiedUp: usd(ccc * cashPerDay, 0),
      _raw: { dio: dio, dso: dso, dpo: dpo, ccc: ccc }
    };
  };

  // 8. Break-even
  C["break-even-calculator"] = function (v) {
    var e = need(v, ["fixed", "price", "variable"]); if (e) return { error: e };
    var cm = v.price - v.variable;
    if (cm <= 0) return { error: "Price must be higher than variable cost per unit, or you never break even." };
    var units = v.fixed / cm, target = v.target || 0;
    return {
      cm: usd(cm), cmr: pct(cm / v.price), units: num(Math.ceil(units)), revenue: usd(units * v.price, 0),
      targetUnits: num(Math.ceil((v.fixed + target) / cm)), targetRevenue: usd((v.fixed + target) / cm * v.price, 0),
      _raw: { units: units, revenue: units * v.price }
    };
  };

  // 9. Borrowing base (AR + inventory)
  C["borrowing-base-calculator"] = function (v) {
    var e = need(v, ["ar", "arAdvance"]); if (e) return { error: e };
    var eligAR = Math.max(0, v.ar - (v.over90 || 0) - (v.arOther || 0));
    var arAvail = eligAR * v.arAdvance / 100;
    var eligInv = Math.max(0, (v.inventory || 0) - (v.invIneligible || 0));
    var invAvail = eligInv * (v.invAdvance || 0) / 100;
    var capped = v.invCap > 0 && invAvail > v.invCap;
    if (capped) invAvail = v.invCap;
    var base = arAvail + invAvail, excess = base - (v.loan || 0);
    return {
      eligAR: usd(eligAR, 0), arAvail: usd(arAvail, 0), eligInv: usd(eligInv, 0),
      invAvail: usd(invAvail, 0) + (capped ? " (capped)" : ""), base: usd(base, 0),
      excess: usd(excess, 0), status: excess >= 0 ? "Available to draw." : "Overadvanced: pay down or add collateral.",
      _raw: { base: base, excess: excess, arAvail: arAvail, invAvail: invAvail }
    };
  };

  // 10. DSO
  C["dso-calculator"] = function (v) {
    var e = need(v, ["ar", "sales", "days"]); if (e) return { error: e };
    if (v.sales <= 0 || v.days <= 0) return { error: "Credit sales and days in period must be above zero." };
    var dso = v.ar / v.sales * v.days, terms = v.terms || 0;
    return {
      dso: num(dso, 1) + " days",
      beyond: terms > 0 ? num(dso - terms, 1) + " days" : "Enter your payment terms",
      daily: usd(v.sales / v.days, 0),
      release: terms > 0 && dso > terms ? usd((dso - terms) * v.sales / v.days, 0) : usd(0, 0),
      _raw: { dso: dso }
    };
  };

  // 11. Margin vs markup
  C["margin-markup-calculator"] = function (v) {
    var e = need(v, ["cost", "price"]); if (e) return { error: e };
    if (v.cost < 0 || v.price <= 0) return { error: "Price must be above zero." };
    var profit = v.price - v.cost, tm = v.targetMargin;
    return {
      profit: usd(profit), margin: pct(profit / v.price), markup: v.cost > 0 ? pct(profit / v.cost) : "—",
      targetPrice: tm > 0 && tm < 100 ? usd(v.cost / (1 - tm / 100)) : "Enter a margin between 0 and 100",
      _raw: { margin: profit / v.price, markup: profit / v.cost, targetPrice: v.cost / (1 - (tm || 0) / 100) }
    };
  };

  // 12. Current and quick ratio
  C["current-ratio-calculator"] = function (v) {
    var e = need(v, ["cash", "ar", "inventory", "cl"]); if (e) return { error: e };
    if (v.cl <= 0) return { error: "Current liabilities must be above zero." };
    var ca = v.cash + v.ar + v.inventory + (v.otherCA || 0);
    return {
      ca: usd(ca, 0), current: (ca / v.cl).toFixed(2), quick: ((v.cash + v.ar) / v.cl).toFixed(2),
      wc: usd(ca - v.cl, 0),
      _raw: { current: ca / v.cl, quick: (v.cash + v.ar) / v.cl, wc: ca - v.cl }
    };
  };

  var api = { calcs: C, pmt: pmt, pv: pv };

  // ---------- browser binding ----------
  if (typeof document !== "undefined") {
    var run = function (form) {
      var fn = C[form.getAttribute("data-calc")]; if (!fn) return;
      var v = {};
      form.querySelectorAll("[name]").forEach(function (el) {
        var raw = String(el.value).replace(/[$,%\s]/g, "");
        v[el.name] = raw === "" ? (el.hasAttribute("data-optional") ? 0 : NaN) : parseFloat(raw);
      });
      var out = fn(v), box = document.querySelector("[data-results='" + form.getAttribute("data-calc") + "']");
      var err = box.querySelector("[data-error]");
      if (out.error) { err.textContent = out.error; err.hidden = false; box.classList.add("is-error"); return; }
      err.hidden = true; box.classList.remove("is-error");
      Object.keys(out).forEach(function (k) {
        if (k.charAt(0) === "_") return;
        var el = box.querySelector("[data-out='" + k + "']"); if (el) el.textContent = out[k];
      });
      var t = document.querySelector("[data-table='" + form.getAttribute("data-calc") + "']");
      if (t && out._table) {
        var h = "<thead><tr>" + out._table.head.map(function (x) { return "<th scope='col'>" + x + "</th>"; }).join("") + "</tr></thead><tbody>";
        out._table.rows.forEach(function (r) { h += "<tr>" + r.map(function (x) { return "<td>" + x + "</td>"; }).join("") + "</tr>"; });
        t.innerHTML = h + "</tbody>";
      }
    };
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll("form[data-calc]").forEach(function (form) {
        form.addEventListener("input", function () { run(form); });
        form.addEventListener("submit", function (ev) { ev.preventDefault(); run(form); });
        run(form);
      });
    });
  }
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CDT = api;
})(this);
