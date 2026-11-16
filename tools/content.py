"""Page content for creditdesktools.com.

Each calculator entry drives one page. Field tuple:
  (name, label, prefix, suffix, default, hint, optional)
Result tuple: (key, label, style) where style is "primary", "" or "note".
The calculator math lives in assets/calc.js under the same slug.
"""

ETSY_SHOP = "https://www.etsy.com/shop/CreditDeskTools"

# Template catalog. Product links point to the Etsy shop until per-listing
# and Payhip URLs are added to ops/CATALOG.md.
TEMPLATES = {
    "loan": ("Loan Readiness Checklist + DSCR Calculator", ETSY_SHOP),
    "cashflow": ("13-Week Cash Flow Forecast", ETSY_SHOP),
    "po": ("PO Financing Deal Calculator", ETSY_SHOP),
    "bb": ("Borrowing Base Certificate", ETSY_SHOP),
    "spread": ("Financial Statement Spreading Template (16 ratios)", ETSY_SHOP),
    "ar": ("AR Aging + DSO Dashboard", ETSY_SHOP),
    "budget": ("Small Business Budget vs Actual", ETSY_SHOP),
    "close": ("Month-End Close Checklist", ETSY_SHOP),
}

GROUPS = [
    ("Borrowing costs", ["business-loan-calculator", "sba-7a-loan-calculator", "mca-apr-calculator", "invoice-factoring-cost-calculator", "po-financing-cost-calculator"]),
    ("Getting approved", ["dscr-calculator", "borrowing-base-calculator", "current-ratio-calculator"]),
    ("Cash flow and working capital", ["cash-conversion-cycle-calculator", "dso-calculator"]),
    ("Pricing and profit", ["break-even-calculator", "margin-markup-calculator"]),
]

CALCS = [
# ---------------------------------------------------------------- 1
dict(
slug="business-loan-calculator",
title="Business Loan Calculator: Monthly Payment and Amortization",
h1="Business Loan Calculator",
card="Monthly payment, total interest and a year-by-year schedule.",
desc="Free business loan calculator. Enter the amount, rate and term to see your monthly payment, total interest and a yearly amortization schedule.",
intro="See the monthly payment on a term loan, what it costs in interest over its life, and how fast the balance comes down.",
fields=[
 ("amount","Loan amount","$","",150000,"",False),
 ("rate","Interest rate","","%",9.5,"Annual rate from your quote",False),
 ("years","Term","","yrs",5,"Most business term loans run 1 to 10 years",False),
],
results=[("payment","Monthly payment","primary"),("totalInterest","Total interest",""),("totalPaid","Total of all payments",""),("year1Interest","Interest in year one","")],
table=True,
formula="Payment = P × r ÷ (1 − (1 + r)^−n)\nP = loan amount, r = annual rate ÷ 12, n = term in months",
template="loan", wfs=False,
related=["sba-7a-loan-calculator","dscr-calculator","mca-apr-calculator"],
guide="""
<h2>How a business term loan payment works</h2>
<p>A term loan is repaid in equal monthly payments. Each payment covers that month's interest first, and whatever is left reduces the balance. Early payments are mostly interest; by the final year almost the whole payment goes to principal. The schedule above shows that shift year by year.</p>
<p>Three inputs drive the payment: the amount borrowed, the annual interest rate, and the number of months. Stretching the term lowers the payment but raises total interest, often by more than people expect. On a $150,000 loan at 9.5%, moving from five to seven years cuts the payment by roughly $700 a month but adds several thousand dollars in interest.</p>

<h2>What the quote leaves out</h2>
<p>The interest rate is not the whole cost. Lenders commonly add an origination fee, a packaging or documentation fee, and sometimes a prepayment penalty. If a fee is deducted from the loan proceeds, you pay interest on money you never receive. To compare offers fairly, ask each lender for the APR, which folds required fees into one annual rate.</p>
<ul>
 <li><strong>Origination fee:</strong> usually a percentage of the loan, paid at closing or taken from proceeds.</li>
 <li><strong>Prepayment penalty:</strong> a charge for paying the loan off early. Ask whether it steps down over time.</li>
 <li><strong>Variable rate:</strong> if the rate floats with prime, your payment can change. Run this calculator at a rate one or two points higher to see the risk.</li>
</ul>

<h2>Can the business afford the payment?</h2>
<p>Lenders answer that question with the debt service coverage ratio: cash flow available for debt divided by total annual debt payments. Most want at least 1.20x to 1.25x. Multiply the monthly payment above by 12, add your other loan payments, and run the <a href="/dscr-calculator/">DSCR calculator</a> before you apply. If the ratio comes up short, a longer term or a smaller amount is easier to fix now than after a decline.</p>

<h2>Using the schedule</h2>
<p>The interest column matters for taxes and budgeting. Business loan interest is generally deductible as a business expense, so your accountant will want the annual interest figure. The ending balance column tells you what it would take to pay the loan off or refinance at the end of any year.</p>
""",
faqs=[
 ("How do I calculate a business loan payment?","Use the standard amortization formula: payment equals the loan amount times the monthly rate, divided by one minus one plus the monthly rate raised to the negative number of months. The calculator does this for you and shows the result as you type."),
 ("Is a longer term better?","A longer term lowers the monthly payment and makes the loan easier to qualify for, but you pay more interest in total. Choose the shortest term your cash flow can comfortably carry."),
 ("Does this include fees?","No. It calculates principal and interest only. Add origination and other fees separately, or ask the lender for the APR to compare offers."),
 ("Is business loan interest tax deductible?","Interest on a loan used for business purposes is generally deductible. Check with your tax preparer for your situation."),
]),
# ---------------------------------------------------------------- 2
dict(
slug="dscr-calculator",
title="DSCR Calculator: Debt Service Coverage Ratio for Business Loans",
h1="DSCR Calculator",
card="Your debt service coverage ratio and the largest loan it supports.",
desc="Free DSCR calculator. See your debt service coverage ratio with a proposed loan and the maximum loan your cash flow supports at a lender's target.",
intro="Check the number lenders look at first: whether your cash flow covers all your loan payments, with room to spare.",
fields=[
 ("noi","Annual cash flow available for debt","$","",180000,"Net operating income or EBITDA",False),
 ("existing","Existing annual debt payments","$","",36000,"Principal + interest on current loans, per year",False),
 ("loan","Proposed new loan","$","",250000,"Enter 0 to test current debt only",True),
 ("rate","New loan rate","","%",9,"",True),
 ("years","New loan term","","yrs",10,"",True),
 ("target","Lender's minimum DSCR","","x",1.25,"1.20 to 1.25 is common",False),
],
results=[("dscr","DSCR","primary"),("verdict","Result","note"),("newDebt","New loan, annual payments",""),("totalDebt","Total annual debt service",""),("maxLoan","Largest new loan at your target","")],
formula="DSCR = Annual cash flow ÷ Total annual debt service\nMax new loan = present value of (cash flow ÷ target − existing debt) over the new loan's term",
template="loan", wfs=False,
related=["business-loan-calculator","sba-7a-loan-calculator","current-ratio-calculator"],
guide="""
<h2>What DSCR measures</h2>
<p>The debt service coverage ratio compares the cash a business generates to the loan payments it owes in a year. A DSCR of 1.00x means every dollar of cash flow goes to debt, with nothing left for a slow month. A DSCR of 1.50x means the business earns $1.50 for every $1.00 of debt payments.</p>
<p>Lenders set a minimum, usually between 1.20x and 1.35x for conventional and SBA loans. Below it, most will decline or cut the loan amount. That is why this calculator also shows the largest new loan your cash flow supports at the lender's target.</p>

<h2>What counts as cash flow</h2>
<p>Lenders start from net income and add back items that don't use cash or won't continue after the loan:</p>
<ul>
 <li>Depreciation and amortization</li>
 <li>Interest expense on debt being refinanced or paid off</li>
 <li>One-time expenses with documentation, such as a legal settlement</li>
 <li>Owner compensation above a market salary, in some cases</li>
</ul>
<p>Some lenders then subtract owner draws, taxes not already deducted, or maintenance capital spending. Be conservative: if an add-back needs a long explanation, assume the lender won't count it.</p>

<h2>What counts as debt service</h2>
<p>Include every required principal and interest payment for the next twelve months: term loans, equipment loans, vehicle loans, SBA loans, and the new loan you are requesting. Lines of credit are often included at an assumed payment even if you only pay interest. Leases may be included too. Leaving debts out only means the lender finds them later.</p>

<h2>Global DSCR</h2>
<p>For small businesses, the owner usually guarantees the loan, so the lender also runs a global DSCR. That combines the business's cash flow with the owner's personal income, then divides by business debt plus personal obligations like a mortgage and car payments. A healthy business can still fail a global test if the owner's personal debt is heavy.</p>

<h2>How to improve a weak DSCR</h2>
<ol>
 <li><strong>Lengthen the term.</strong> A 10-year loan has a much lower annual payment than a 5-year loan of the same size.</li>
 <li><strong>Borrow less.</strong> Use the maximum loan figure above as your ceiling.</li>
 <li><strong>Refinance expensive debt.</strong> Rolling a short, high-payment loan into the new one can raise the ratio.</li>
 <li><strong>Document add-backs.</strong> Clean books with clear support let the lender count cash flow they would otherwise ignore.</li>
</ol>
""",
faqs=[
 ("What is a good DSCR?","Most lenders want at least 1.20x to 1.25x. Above 1.50x is considered strong. Below 1.00x means cash flow does not cover the payments."),
 ("Is DSCR calculated with EBITDA or net income?","Lenders typically start with net income and add back depreciation, amortization, interest and documented one-time items, which lands close to EBITDA. Each lender has its own adjustments."),
 ("Does DSCR include the new loan?","Yes. Lenders calculate DSCR on a pro forma basis, including the payment on the loan you are applying for along with your existing debt."),
 ("What is the difference between DSCR and global DSCR?","DSCR uses only the business's cash flow and debt. Global DSCR adds the guarantor's personal income and personal debt payments."),
]),
# ---------------------------------------------------------------- 3
dict(
slug="sba-7a-loan-calculator",
title="SBA 7(a) Loan Calculator: Monthly Payment With Guarantee Fee",
h1="SBA 7(a) Loan Calculator",
card="Payment on an SBA 7(a) loan, with the guarantee fee financed in.",
desc="Free SBA 7(a) loan calculator. Estimate the monthly payment and total interest, including an optional guarantee fee added to the loan.",
intro="Estimate the payment on an SBA 7(a) loan, including the guarantee fee if it is rolled into the loan.",
fields=[
 ("amount","Loan amount","$","",350000,"7(a) loans go up to $5 million",False),
 ("rate","Interest rate","","%",10.5,"Most 7(a) rates are prime plus a spread",False),
 ("years","Term","","yrs",10,"Typically 10 years; up to 25 for real estate",False),
 ("feePct","Guarantee fee financed","","%",0,"Optional. Use the current SBA fee for your loan size",True),
],
results=[("payment","Monthly payment","primary"),("fee","Guarantee fee",""),("principal","Total financed",""),("totalInterest","Total interest",""),("totalPaid","Total of all payments","")],
formula="Financed = Loan + (Loan × guarantee fee %)\nPayment = Financed × r ÷ (1 − (1 + r)^−n), r = rate ÷ 12, n = months",
template="loan", wfs=False,
related=["business-loan-calculator","dscr-calculator","break-even-calculator"],
guide="""
<h2>How SBA 7(a) loans are structured</h2>
<p>The 7(a) program is the SBA's main small business loan. A bank or other approved lender makes the loan, and the SBA guarantees a portion of it, which lets the lender offer longer terms than a conventional loan. The maximum loan amount is $5 million.</p>
<p>Terms depend on what the money is for. Working capital and equipment loans commonly run up to 10 years. Loans that finance real estate can run up to 25 years. Longer terms mean lower payments, which is often the main reason a business chooses SBA financing over a conventional term loan.</p>

<h2>Rates</h2>
<p>Most 7(a) loans carry a variable rate set at the prime rate plus a spread, and the SBA caps how large that spread can be. Because the rate floats, your payment can change when prime moves. Run the calculator at your quoted rate, then again one or two points higher, to see how much room your cash flow has if rates rise.</p>

<h2>The guarantee fee</h2>
<p>The SBA charges the lender a guarantee fee on the guaranteed portion of the loan, and the lender usually passes it to the borrower. The fee percentage depends on loan size and maturity, and the SBA resets it each fiscal year, so check the current schedule or ask your lender for the exact figure. Many borrowers finance the fee into the loan rather than paying it at closing. Enter the fee as a percentage of the loan amount above to see its effect on the payment.</p>

<h2>What else to expect</h2>
<ul>
 <li><strong>Personal guarantee:</strong> owners of 20% or more generally guarantee the loan.</li>
 <li><strong>Collateral:</strong> lenders take available business assets, and sometimes personal real estate, for larger loans.</li>
 <li><strong>Equity injection:</strong> for acquisitions and startups, expect to put in some of your own cash.</li>
 <li><strong>Prepayment fee:</strong> loans of 15 years or longer can carry a fee if paid off early in the first three years.</li>
 <li><strong>Paperwork:</strong> tax returns, interim financials, a debt schedule and a personal financial statement.</li>
</ul>

<h2>Will you qualify?</h2>
<p>SBA lenders focus on repayment ability. Take the monthly payment above, multiply by 12, add your other debt payments, and test the total in the <a href="/dscr-calculator/">DSCR calculator</a>. Most lenders look for 1.15x to 1.25x or better.</p>
""",
faqs=[
 ("What is the current SBA 7(a) interest rate?","Most 7(a) loans use the prime rate plus a spread capped by the SBA, so the rate changes when prime changes. Ask lenders for current quotes and enter the rate above."),
 ("How long is an SBA 7(a) loan term?","Up to 10 years for working capital and equipment is typical, and up to 25 years when the loan finances real estate."),
 ("Can the SBA guarantee fee be financed?","Usually, yes. Many borrowers add the fee to the loan amount. Enter the fee percentage above to see the effect on your payment."),
 ("What is the maximum SBA 7(a) loan?","The program maximum is $5 million."),
]),
# ---------------------------------------------------------------- 4
dict(
slug="invoice-factoring-cost-calculator",
title="Invoice Factoring Cost Calculator: Fees, Rebate and True APR",
h1="Invoice Factoring Cost Calculator",
card="What factoring an invoice really costs, as dollars and as an APR.",
desc="Free invoice factoring calculator. See the advance, factoring fee, rebate and effective annual rate for any invoice, fee rate and payment timeline.",
intro="Turn a factoring quote into real numbers: what you get today, what the factor keeps, and the annualized cost.",
fields=[
 ("invoice","Invoice amount","$","",25000,"",False),
 ("advance","Advance rate","","%",85,"Share of the invoice paid up front",False),
 ("fee","Factoring fee","","%",2.5,"Per fee period",False),
 ("period","Fee period","","days",30,"How often the fee is charged",False),
 ("days","Days until your customer pays","","days",45,"",False),
],
results=[("apr","Effective annual rate","primary"),("advanceAmt","Cash advanced today",""),("feeAmt","Factoring fee",""),("periods","Fee periods charged",""),("rebate","Rebate when customer pays","")],
formula="Fee periods = days to pay ÷ fee period, rounded up\nFee = Invoice × fee % × periods\nRebate = Invoice − advance − fee\nEffective annual rate = Fee ÷ advance × 365 ÷ days",
template="ar", wfs=True,
related=["dso-calculator","po-financing-cost-calculator","borrowing-base-calculator"],
guide="""
<h2>How invoice factoring works</h2>
<p>Factoring turns unpaid invoices into cash before your customer pays. You sell the invoice to a factor, which advances most of its value right away, usually 70% to 90%. When your customer pays the factor, it releases the remainder to you, minus its fee. That remainder is called the rebate or reserve.</p>
<p>Because the factor is relying on your customer's credit, factoring is often available to young or thinly capitalized businesses that can't get a bank line. The trade-off is cost.</p>

<h2>Why the quoted rate understates the cost</h2>
<p>A factor might quote "2.5% per 30 days." That sounds cheap next to a 10% bank loan, but the two are not on the same basis:</p>
<ul>
 <li><strong>The fee is charged on the full invoice,</strong> while you only receive the advance. You pay on money you haven't received yet.</li>
 <li><strong>Fees are charged by period, rounded up.</strong> If your customer pays on day 31 of a 30-day period, you usually pay for two full periods.</li>
 <li><strong>The rate is per month, not per year.</strong> 2.5% every 30 days is about 30% a year before the other two effects.</li>
</ul>
<p>The effective annual rate above puts the cost on the same footing as a loan APR so you can compare honestly.</p>

<h2>Read the agreement for these terms</h2>
<ul>
 <li><strong>Recourse vs non-recourse:</strong> with recourse, you buy back invoices your customer doesn't pay. Non-recourse shifts some credit risk to the factor, usually only for customer insolvency, and costs more.</li>
 <li><strong>Minimum volume:</strong> some agreements charge you if you factor less than a set amount each month.</li>
 <li><strong>Extra fees:</strong> application, due diligence, wire, lockbox and termination fees all add to the true cost.</li>
 <li><strong>Notification:</strong> your customers will usually be told to pay the factor directly.</li>
</ul>

<h2>When factoring makes sense</h2>
<p>Factoring can be worth the cost when it lets you take orders you would otherwise turn down, or when the alternative is a merchant cash advance. It is expensive as a permanent solution. If your customers routinely pay late, start by checking your <a href="/dso-calculator/">days sales outstanding</a> and tightening collections, which frees cash at no cost. Once you have steady receivables and clean books, an asset-based line of credit is usually far cheaper.</p>
""",
faqs=[
 ("What is a typical factoring rate?","Fees commonly run from about 1% to 5% per 30 days, depending on volume, your customers' credit and how quickly they pay."),
 ("Is factoring a loan?","Usually not. You are selling the invoice rather than borrowing against it, which is why it can be easier to get than a loan. The cost still behaves like interest."),
 ("What is a factoring rebate?","The rebate, or reserve, is the part of the invoice the factor holds back until your customer pays. You receive it minus the factoring fee."),
 ("Why is the effective rate so much higher than the quoted fee?","The fee is charged per period, on the full invoice rather than the cash advanced, and periods are rounded up. Annualizing it on the advance shows the real cost."),
]),
# ---------------------------------------------------------------- 5
dict(
slug="po-financing-cost-calculator",
title="Purchase Order Financing Calculator: Cost and Profit Impact",
h1="Purchase Order Financing Calculator",
card="Whether a PO-financed order still makes money after financing costs.",
desc="Free purchase order financing calculator. See financing cost, profit after financing, margin and effective annual rate for a PO-funded order.",
intro="Before you accept PO financing, check that the order still earns enough after the funder is paid.",
fields=[
 ("supplier","Supplier cost of the order","$","",80000,"What you owe your supplier",False),
 ("funding","Share of supplier cost funded","","%",100,"Many funders cover 80% to 100%",False),
 ("fee","Financing fee","","%",3,"Per 30 days",False),
 ("days","Days until funder is repaid","","days",75,"Supplier payment through customer payment",False),
 ("sale","Customer sale price","$","",120000,"",False),
 ("other","Other order costs","$","",6000,"Freight, duties, packaging",True),
],
results=[("after","Profit after financing","primary"),("cost","Financing cost",""),("before","Profit before financing",""),("margin","Margin after financing",""),("share","Share of profit to financing",""),("apr","Effective annual rate",""),("funded","Amount funded","")],
formula="Financing cost = Supplier cost × funded % × fee % × periods (30-day periods, rounded up)\nProfit after = Sale − supplier cost − other costs − financing cost\nEffective annual rate = Cost ÷ amount funded × 365 ÷ days",
template="po", wfs=False,
related=["invoice-factoring-cost-calculator","margin-markup-calculator","cash-conversion-cycle-calculator"],
guide="""
<h2>What purchase order financing does</h2>
<p>PO financing pays your supplier so you can fill a confirmed customer order you couldn't otherwise afford. The funder pays the supplier directly, the goods ship to your customer, you invoice, and the invoice is usually factored or paid to the funder. Once the funder is repaid with its fees, the remaining profit is yours.</p>
<p>It fits resellers, distributors, importers and wholesalers with large orders from creditworthy customers, usually where the goods are finished products that ship without much work by you. It is rarely available for services or for products you manufacture yourself.</p>

<h2>Why the timeline matters most</h2>
<p>PO fees are charged by time, so the number that moves the result most is how long the money is out. That clock starts when the funder pays your supplier and stops when the funder is repaid. It includes production time, shipping, your customer's receiving and inspection, and your customer's payment terms. A 30-day delay at the port can add a whole fee period.</p>
<p>Enter a realistic day count, then try it again with 30 more days. If the order only works on the optimistic timeline, it is a risky order.</p>

<h2>Margin is the gate</h2>
<p>Funders generally want gross margins of 20% or more before financing, because their fees and any factoring costs come out of that margin. Run this calculator and look at two lines:</p>
<ul>
 <li><strong>Profit after financing:</strong> is it still worth the work and the risk?</li>
 <li><strong>Share of profit to financing:</strong> if the funder takes more than about half of your profit, consider negotiating a deposit from your customer or better supplier terms.</li>
</ul>

<h2>Reduce what you finance</h2>
<ol>
 <li>Ask your customer for a deposit with the order.</li>
 <li>Ask your supplier for partial terms, such as 30% down and the balance on shipment.</li>
 <li>Shorten the timeline by shipping faster or invoicing sooner.</li>
 <li>Factor the receivable rather than waiting the full payment term, if that is cheaper.</li>
</ol>

<h2>What funders look for</h2>
<p>Expect questions about your customer's creditworthiness, your supplier's track record, the purchase order itself, and how the goods move. A clear deal file with the PO, supplier quote, shipping plan and your margin math gets faster answers.</p>
""",
faqs=[
 ("How much does purchase order financing cost?","Fees often run from about 1.5% to 6% per 30 days on the amount funded. Because fees accrue over time, the total depends on how long the funder is out of pocket."),
 ("What margin do I need for PO financing?","Most funders look for gross margins of at least 20% so the order is still profitable after their fees."),
 ("Is PO financing the same as factoring?","No. PO financing pays your supplier before goods ship. Factoring advances cash against an invoice after goods are delivered. Many deals use both."),
 ("Who qualifies for PO financing?","Businesses reselling finished goods to creditworthy commercial or government customers, with a reliable supplier and a confirmed purchase order."),
]),
# ---------------------------------------------------------------- 6
dict(
slug="mca-apr-calculator",
title="Merchant Cash Advance APR Calculator: Find the True Cost",
h1="Merchant Cash Advance APR Calculator",
card="Convert an MCA factor rate into a true annual percentage rate.",
desc="Free merchant cash advance calculator. Convert a factor rate and daily or weekly payment into total cost, payoff time and true APR.",
intro="A merchant cash advance quotes a factor rate, not an interest rate. This converts it into a true annual rate you can compare.",
fields=[
 ("funded","Advance amount","$","",50000,"",False),
 ("factor","Factor rate","","",1.35,"Total payback ÷ amount advanced",False),
 ("fees","Fees deducted from funding","$","",1500,"Origination, underwriting",True),
 ("payment","Payment amount","$","",535.71,"Per daily or weekly debit",False),
],
select=("freq","Payment frequency",[("252","Daily (business days)"),("52","Weekly")],"Daily payments are usually on business days only"),
results=[("apr","True APR","primary"),("payback","Total payback",""),("cost","Total cost of the advance",""),("count","Number of payments",""),("term","Estimated payoff time","")],
formula="Payback = Advance × factor rate\nPayments = Payback ÷ payment amount\nTrue APR = the periodic rate that makes the payments equal the net cash received, × payments per year",
template="cashflow", wfs=True,
related=["business-loan-calculator","invoice-factoring-cost-calculator","cash-conversion-cycle-calculator"],
guide="""
<h2>Factor rates are not interest rates</h2>
<p>A merchant cash advance (MCA) is sold as a purchase of your future sales. The provider gives you a lump sum and collects a larger fixed amount, the payback, through daily or weekly debits from your bank account. The cost is quoted as a factor rate, such as 1.35, meaning you repay $1.35 for every $1 advanced.</p>
<p>A factor rate of 1.35 sounds like 35%, but that is the total cost, not an annual rate. If you repay in six months, the annualized cost is far higher than 35%, because you are paying it back quickly and the balance shrinks with every debit while the cost stays fixed.</p>

<h2>How this calculator finds the true APR</h2>
<p>It takes the cash you actually receive (the advance minus any fees taken out up front), the fixed payment, and the number of payments needed to reach the payback. It then solves for the interest rate that makes that stream of payments equal to the cash received, the same method used to calculate a loan's APR, and annualizes it. Triple-digit results are common for MCAs.</p>

<h2>Paying it off early usually doesn't save money</h2>
<p>With a loan, paying early cuts the interest. With most MCAs, the payback amount is fixed, so paying early only raises the effective rate. Some providers offer an early payoff discount; ask for it in writing before you sign.</p>

<h2>Watch out for stacking</h2>
<p>Taking a second advance to cover the payments on the first is called stacking. It is the most common way businesses get into serious trouble with MCAs: daily debits from two or three providers can consume most of the cash coming in. If you are considering a second advance, step back and look at your cash flow first.</p>

<h2>Alternatives worth checking first</h2>
<ul>
 <li>A business line of credit or term loan, even at a high rate, usually costs a fraction of an MCA.</li>
 <li><a href="/invoice-factoring-cost-calculator/">Invoice factoring</a>, if you sell to other businesses on terms.</li>
 <li>Negotiating longer terms with suppliers or faster payment from customers.</li>
 <li>A 13-week cash flow forecast, to see whether the shortfall is temporary or structural before you commit to daily payments.</li>
</ul>
""",
faqs=[
 ("What is a factor rate?","The total amount you repay divided by the amount advanced. A 1.35 factor rate on $50,000 means you repay $67,500."),
 ("How do I convert a factor rate to APR?","Find the rate that makes the series of fixed payments equal the cash you received, then multiply by the number of payments per year. The calculator does this automatically."),
 ("Why is MCA APR so high?","The cost is fixed and repaid over a short period through frequent payments, so the annualized rate is much higher than the factor rate suggests."),
 ("Can I pay off a merchant cash advance early to save money?","Usually not, because the payback amount is fixed. Some providers offer an early payoff discount, so ask before you sign."),
]),
# ---------------------------------------------------------------- 7
dict(
slug="cash-conversion-cycle-calculator",
title="Cash Conversion Cycle Calculator: DIO, DSO and DPO",
h1="Cash Conversion Cycle Calculator",
card="How many days your cash is tied up in inventory and receivables.",
desc="Free cash conversion cycle calculator. Enter revenue, cost of goods, inventory, receivables and payables to get DIO, DSO, DPO and your cash cycle in days.",
intro="Measure how long each dollar spent on inventory takes to come back as cash from customers.",
fields=[
 ("revenue","Annual revenue","$","",1800000,"",False),
 ("cogs","Annual cost of goods sold","$","",1100000,"",False),
 ("inventory","Inventory","$","",210000,"Average or current balance",False),
 ("ar","Accounts receivable","$","",240000,"",False),
 ("ap","Accounts payable","$","",120000,"",False),
],
results=[("ccc","Cash conversion cycle","primary"),("dio","Days inventory outstanding",""),("dso","Days sales outstanding",""),("dpo","Days payables outstanding",""),("tiedUp","Cash tied up in the cycle","")],
formula="DIO = Inventory ÷ COGS × 365\nDSO = Receivables ÷ Revenue × 365\nDPO = Payables ÷ COGS × 365\nCash conversion cycle = DIO + DSO − DPO",
template="spread", wfs=True,
related=["dso-calculator","current-ratio-calculator","break-even-calculator"],
guide="""
<h2>What the cash conversion cycle tells you</h2>
<p>The cash conversion cycle (CCC) measures how many days pass between paying for inventory and collecting cash from the customer who bought it. A 55-day cycle means every dollar you put into inventory is unavailable for about 55 days. The longer the cycle, the more working capital the business needs, and the more it has to borrow as it grows.</p>
<p>The cycle has three parts:</p>
<ul>
 <li><strong>Days inventory outstanding (DIO):</strong> how long inventory sits before it sells.</li>
 <li><strong>Days sales outstanding (DSO):</strong> how long customers take to pay.</li>
 <li><strong>Days payables outstanding (DPO):</strong> how long you take to pay suppliers. This one shortens the cycle, because your suppliers are financing you in the meantime.</li>
</ul>

<h2>Why growing businesses run out of cash</h2>
<p>A profitable business can still run short of cash if its cycle is long. Each new sale requires buying inventory now and collecting later. The "cash tied up" figure above estimates how much money is locked in the cycle at your current cost base. If sales grow 25%, that figure grows about 25% too, and the cash has to come from somewhere.</p>

<h2>Ways to shorten the cycle</h2>
<ol>
 <li><strong>Collect faster:</strong> invoice on the day you ship, offer card or ACH payment, follow up on day one past due, and consider a small early-payment discount.</li>
 <li><strong>Carry less inventory:</strong> find slow-moving items and stop reordering them; order more often in smaller quantities.</li>
 <li><strong>Pay on terms, not early:</strong> negotiate 45 or 60 days with key suppliers and use the full term, unless an early-pay discount is worth more.</li>
</ol>
<p>Even a few days off the cycle can free a meaningful amount of cash. At $1.1 million in annual cost of goods, each day is worth about $3,000.</p>

<h2>Using the right numbers</h2>
<p>Use a full year of revenue and cost of goods sold, and average balances for inventory, receivables and payables if your business is seasonal. A single month-end balance can make the cycle look better or worse than it is. Lenders who finance working capital, especially asset-based lenders, look at these same measures.</p>
""",
faqs=[
 ("What is a good cash conversion cycle?","It depends on the industry. Retailers and distributors often run 30 to 90 days; businesses paid up front can run negative. Compare yourself to your own trend and to peers."),
 ("Can the cash conversion cycle be negative?","Yes. If customers pay before you pay suppliers, the cycle is negative and suppliers are effectively funding your growth."),
 ("Should I use revenue or cost of goods sold for DIO?","Use cost of goods sold for DIO and DPO, since inventory and payables are carried at cost, and revenue for DSO."),
 ("How often should I calculate the cycle?","Quarterly is a good habit, monthly if cash is tight or you are growing fast."),
]),
# ---------------------------------------------------------------- 8
dict(
slug="break-even-calculator",
title="Break-Even Calculator: Units and Sales to Cover Your Costs",
h1="Break-Even Calculator",
card="Units and revenue needed to cover fixed costs, or hit a profit goal.",
desc="Free break-even calculator for small businesses. Find the units and sales revenue needed to cover fixed costs and reach a target profit.",
intro="Find how much you need to sell each month to cover your costs, and what it takes to reach a profit goal.",
fields=[
 ("fixed","Monthly fixed costs","$","",24000,"Rent, salaries, insurance, software",False),
 ("price","Price per unit","$","",85,"",False),
 ("variable","Variable cost per unit","$","",49,"Materials, shipping, payment fees",False),
 ("target","Monthly profit goal","$","",5000,"",True),
],
results=[("units","Break-even units per month","primary"),("revenue","Break-even sales",""),("cm","Contribution per unit",""),("cmr","Contribution margin",""),("targetUnits","Units to reach profit goal",""),("targetRevenue","Sales to reach profit goal","")],
formula="Contribution per unit = Price − variable cost\nBreak-even units = Fixed costs ÷ contribution per unit\nUnits for a profit goal = (Fixed costs + goal) ÷ contribution per unit",
template="budget", wfs=True,
related=["margin-markup-calculator","cash-conversion-cycle-calculator","business-loan-calculator"],
guide="""
<h2>What break-even means</h2>
<p>Your break-even point is the level of sales where total revenue equals total costs, so you neither make nor lose money. Every sale above it adds profit; every sale below it adds to a loss. Knowing the number turns a vague goal like "sell more" into a specific monthly target.</p>

<h2>Fixed and variable costs</h2>
<p>The calculation depends on splitting your costs correctly:</p>
<ul>
 <li><strong>Fixed costs</strong> stay the same whether you sell one unit or a thousand in a month: rent, salaried staff, insurance, software, loan payments.</li>
 <li><strong>Variable costs</strong> rise with each unit sold: materials, packaging, shipping, sales commissions, card processing fees.</li>
</ul>
<p>Some costs are mixed. Hourly labor might be fixed up to a point and then rise with volume. Make a reasonable split and note your assumptions.</p>

<h2>Contribution margin is the key number</h2>
<p>Each unit's price minus its variable cost is its contribution, the amount it adds toward fixed costs and profit. Divide fixed costs by contribution and you have break-even units. A low contribution margin means a small price cut or cost increase moves break-even a long way. Try lowering the price in the calculator by 5% and watch the break-even units change.</p>

<h2>Using it for decisions</h2>
<ol>
 <li><strong>Pricing:</strong> see how many more units a discount requires to earn the same profit.</li>
 <li><strong>Hiring or new rent:</strong> add the new fixed cost and see how many extra units cover it.</li>
 <li><strong>Loans:</strong> include the monthly payment from the <a href="/business-loan-calculator/">business loan calculator</a> in fixed costs before you borrow.</li>
 <li><strong>New products:</strong> test whether a product line can realistically reach its own break-even.</li>
</ol>

<h2>For businesses with many products</h2>
<p>If you sell many items at different prices, use averages: average selling price and average variable cost per sale, or work in revenue terms using your overall contribution margin percentage. Break-even sales equal fixed costs divided by that percentage.</p>
""",
faqs=[
 ("How do I calculate break-even point?","Divide fixed costs by the contribution per unit, which is price minus variable cost per unit. The result is the number of units you must sell to cover costs."),
 ("What if I sell services instead of products?","Use billable hours or jobs as the unit. Price is your rate per hour or job, and variable cost is the direct cost of delivering it."),
 ("Should loan payments be in fixed costs?","For cash planning, yes. Include the full monthly payment so the break-even reflects the cash you need."),
 ("Why does a small price cut change break-even so much?","A price cut comes entirely out of contribution margin, so each unit covers less of your fixed costs and you need more units."),
]),
# ---------------------------------------------------------------- 9
dict(
slug="borrowing-base-calculator",
title="Borrowing Base Calculator: AR and Inventory Availability",
h1="Borrowing Base Calculator",
card="How much an asset-based line of credit lets you draw today.",
desc="Free borrowing base calculator. Work out eligible receivables and inventory, advance rates and availability on an asset-based line of credit.",
intro="Work out how much you can draw on an asset-based line of credit from your receivables and inventory.",
fields=[
 ("ar","Total accounts receivable","$","",600000,"",False),
 ("over90","Past due over 90 days","$","",45000,"Usually ineligible",True),
 ("arOther","Other ineligible receivables","$","",25000,"Affiliates, foreign, contra, concentration",True),
 ("arAdvance","Receivables advance rate","","%",85,"",False),
 ("inventory","Inventory","$","",400000,"",True),
 ("invIneligible","Ineligible inventory","$","",60000,"Slow-moving, work in process, consigned",True),
 ("invAdvance","Inventory advance rate","","%",50,"",True),
 ("invCap","Inventory cap","$","",150000,"Maximum loan against inventory; 0 for none",True),
 ("loan","Current loan balance","$","",450000,"",True),
],
results=[("excess","Available to draw","primary"),("status","Status","note"),("base","Borrowing base",""),("eligAR","Eligible receivables",""),("arAvail","Availability from receivables",""),("eligInv","Eligible inventory",""),("invAvail","Availability from inventory","")],
formula="Eligible AR = Total AR − over 90 days − other ineligibles\nBorrowing base = Eligible AR × AR rate + min(Eligible inventory × inventory rate, cap)\nAvailable = Borrowing base − loan balance",
template="bb", wfs=False,
related=["dso-calculator","invoice-factoring-cost-calculator","current-ratio-calculator"],
guide="""
<h2>What a borrowing base is</h2>
<p>An asset-based line of credit doesn't have a fixed limit you can always draw. Instead, the amount available moves with your collateral. The borrowing base is the lender's calculation of what your receivables and inventory will support, and you report it on a borrowing base certificate, usually weekly or monthly. You can draw up to the lesser of the borrowing base or the line's maximum.</p>

<h2>Eligible receivables</h2>
<p>Lenders only lend against receivables they expect to collect. Common exclusions include:</p>
<ul>
 <li>Invoices more than 90 days past invoice date, or 60 days past due</li>
 <li>Cross-aging: all of a customer's invoices if a large share are past due</li>
 <li>Amounts owed by affiliates, employees or related companies</li>
 <li>Foreign customers without credit insurance</li>
 <li>Contra accounts, where you also owe the customer money</li>
 <li>Concentrations above a limit, often 20% to 25% in one customer</li>
</ul>
<p>The advance rate on eligible receivables is usually 75% to 90%.</p>

<h2>Eligible inventory</h2>
<p>Inventory is harder for a lender to turn into cash, so advance rates are lower, often 25% to 65% of cost, and an inventory cap limits the total. Finished goods are generally eligible; work in process, slow-moving stock and consigned goods usually are not. Many lenders base the rate on an appraisal of what the inventory would bring in a liquidation.</p>

<h2>Overadvances and reserves</h2>
<p>If your loan balance is higher than the borrowing base, you are overadvanced and must pay the difference down. That can happen without any new borrowing, simply because receivables were collected faster than new invoices came in, or because a large customer went past 90 days. Lenders can also add reserves, for example for rent owed at a warehouse or for taxes, which reduce availability further.</p>

<h2>Keeping availability healthy</h2>
<ol>
 <li>Keep collections current. Every invoice that ages past 90 days drops out entirely.</li>
 <li>Watch customer concentration as one account grows.</li>
 <li>Report accurately and on time. Errors on a certificate damage the lender's trust quickly.</li>
 <li>Track your <a href="/dso-calculator/">days sales outstanding</a> so you see aging problems before the lender does.</li>
</ol>
""",
faqs=[
 ("What is a typical advance rate on receivables?","Usually 75% to 90% of eligible receivables, depending on customer quality and dilution history."),
 ("Why are invoices over 90 days ineligible?","The older an invoice gets, the less likely it is to be collected, so lenders exclude it from the collateral they lend against."),
 ("What is an inventory cap?","A dollar limit on how much of the borrowing base can come from inventory, regardless of how much inventory you have."),
 ("What happens if I am overadvanced?","You must repay the amount above the borrowing base, usually promptly. Repeated overadvances can be a default under the loan agreement."),
]),
# ---------------------------------------------------------------- 10
dict(
slug="dso-calculator",
title="DSO Calculator: Days Sales Outstanding",
h1="DSO Calculator",
card="How many days customers take to pay, and the cash a faster pace frees.",
desc="Free days sales outstanding (DSO) calculator. See how long customers take to pay, how far that runs past your terms, and how much cash collections could free.",
intro="Measure how long your customers take to pay you, and how much cash you would free by collecting on terms.",
fields=[
 ("ar","Accounts receivable","$","",185000,"Balance at period end",False),
 ("sales","Credit sales in the period","$","",1300000,"",False),
 ("days","Days in the period","","days",365,"365 for a year, 90 for a quarter",False),
 ("terms","Your payment terms","","days",30,"Optional, e.g. net 30",True),
],
results=[("dso","Days sales outstanding","primary"),("beyond","Days beyond terms",""),("release","Cash freed by collecting on terms",""),("daily","Average credit sales per day","")],
formula="DSO = Accounts receivable ÷ credit sales × days in period\nCash freed = (DSO − terms) × credit sales per day",
template="ar", wfs=True,
related=["cash-conversion-cycle-calculator","borrowing-base-calculator","invoice-factoring-cost-calculator"],
guide="""
<h2>What DSO measures</h2>
<p>Days sales outstanding is the average number of days it takes to collect payment after a sale on credit. If your terms are net 30 and your DSO is 52, customers are paying, on average, about three weeks late. That gap is cash you have earned but can't use.</p>
<p>The "cash freed" figure above estimates how much money would come in if your DSO matched your terms. For many small businesses it is the single largest source of cash available without borrowing.</p>

<h2>Calculating it correctly</h2>
<ul>
 <li><strong>Use credit sales, not total sales.</strong> Cash and card sales collected at the point of sale never become receivables and make DSO look better than it is.</li>
 <li><strong>Match the period.</strong> Quarterly sales with 90 days, or annual sales with 365.</li>
 <li><strong>Watch seasonality.</strong> A big sales month at period end raises receivables and DSO even if customers pay on time. Compare the same month across years, or use average receivables.</li>
</ul>

<h2>DSO and the aging report together</h2>
<p>DSO is an average, so it can hide problems. One large customer 120 days late can sit inside a DSO that looks acceptable. Pair DSO with an aging report that shows balances in current, 1-30, 31-60, 61-90 and over-90 buckets. Lenders do the same: receivables over 90 days are usually excluded from a <a href="/borrowing-base-calculator/">borrowing base</a>.</p>

<h2>How to bring DSO down</h2>
<ol>
 <li><strong>Invoice immediately.</strong> Every day between shipping and invoicing adds a day to DSO.</li>
 <li><strong>Make paying easy.</strong> Accept ACH and cards, and put a payment link on every invoice.</li>
 <li><strong>Follow up on a schedule.</strong> A friendly reminder before the due date, a call on day one past due, and escalation at 30 days past due.</li>
 <li><strong>Set terms per customer.</strong> Give new or slow customers shorter terms, or ask for deposits.</li>
 <li><strong>Stop shipping to chronic late payers</strong> until their balance is current.</li>
</ol>
<p>If your DSO stays high because your customers are large companies that pay slowly by policy, factoring or an asset-based line can bridge the gap, at a cost.</p>
""",
faqs=[
 ("What is a good DSO?","Close to your payment terms. A DSO within about 10 to 15 days of your terms is generally healthy; much higher means collections need attention."),
 ("Should DSO use total sales or credit sales?","Credit sales. Including cash sales understates how long credit customers take to pay."),
 ("How is DSO different from the cash conversion cycle?","DSO measures only collections. The cash conversion cycle adds inventory days and subtracts the days you take to pay suppliers."),
 ("Why did my DSO jump at month end?","A large amount of sales at the end of the period raises receivables before customers have had time to pay. Compare to the same period last year or use average receivables."),
]),
# ---------------------------------------------------------------- 11
dict(
slug="margin-markup-calculator",
title="Margin vs Markup Calculator: Price, Margin and Markup",
h1="Margin vs Markup Calculator",
card="Gross margin and markup from cost and price, or price from a target margin.",
desc="Free margin and markup calculator. Find gross margin and markup from cost and price, and the price needed to hit a target margin.",
intro="See your gross margin and markup side by side, and the price you need to hit a target margin.",
fields=[
 ("cost","Cost per unit","$","",42,"",False),
 ("price","Selling price","$","",70,"",False),
 ("targetMargin","Target gross margin","","%",45,"",True),
],
results=[("margin","Gross margin","primary"),("markup","Markup",""),("profit","Gross profit per unit",""),("targetPrice","Price for target margin","")],
formula="Gross margin = (Price − cost) ÷ price\nMarkup = (Price − cost) ÷ cost\nPrice for a target margin = Cost ÷ (1 − target margin)",
template="budget", wfs=True,
related=["break-even-calculator","po-financing-cost-calculator","cash-conversion-cycle-calculator"],
guide="""
<h2>Margin and markup are not the same</h2>
<p>Both describe the gap between what something costs and what it sells for, but they divide by different numbers:</p>
<ul>
 <li><strong>Markup</strong> divides profit by cost. Buy for $60, sell for $100, and the markup is 67%.</li>
 <li><strong>Margin</strong> divides profit by price. The same item has a 40% gross margin.</li>
</ul>
<p>Mixing them up is one of the most common pricing mistakes. If you want a 40% margin and add 40% to cost, you end up with a 28.6% margin, and over a year that difference can wipe out most of your profit.</p>

<h2>Pricing to a target margin</h2>
<p>To hit a target margin, divide cost by one minus the margin. For a 45% margin on a $42 item: $42 ÷ 0.55 = $76.36. The calculator does this in the last result line. Working from margin keeps your pricing tied to the number on your income statement.</p>

<h2>Quick conversion table</h2>
<p>Common pairs to keep in mind: a 25% markup equals a 20% margin; 50% markup equals 33.3% margin; 100% markup equals 50% margin; 150% markup equals 60% margin. Markup is always the larger number, because cost is always smaller than price.</p>

<h2>Which costs belong in "cost"</h2>
<p>Use the full landed cost of the item: the purchase price plus freight in, duties, and packaging. For a service, use the direct labor and materials to deliver it. Overhead like rent and salaries does not go here; it is covered by gross profit and shows up in your <a href="/break-even-calculator/">break-even</a>.</p>

<h2>Why margin matters to lenders</h2>
<p>Gross margin is one of the first numbers a lender or financing partner checks. Purchase order funders usually want 20% or more, and a falling margin across years raises questions in any credit review. Track it monthly and investigate any drop.</p>
""",
faqs=[
 ("What is the difference between margin and markup?","Markup is profit divided by cost. Margin is profit divided by selling price. The same sale always has a higher markup percentage than margin percentage."),
 ("How do I convert markup to margin?","Margin equals markup divided by one plus markup. A 50% markup is 0.5 ÷ 1.5, or a 33.3% margin."),
 ("How do I price for a 50% margin?","Divide the cost by 0.5, which doubles it. A $30 cost needs a $60 price for a 50% margin."),
 ("What is a good gross margin?","It varies widely by industry. Distributors may run 15% to 30%; software and services can exceed 60%. Compare to your own history and industry peers."),
]),
# ---------------------------------------------------------------- 12
dict(
slug="current-ratio-calculator",
title="Current Ratio and Quick Ratio Calculator",
h1="Current and Quick Ratio Calculator",
card="Liquidity ratios lenders check: current, quick and working capital.",
desc="Free current ratio and quick ratio calculator. Enter current assets and liabilities to get both liquidity ratios and your working capital.",
intro="Check whether your short-term assets cover your short-term bills, the way a lender reads your balance sheet.",
fields=[
 ("cash","Cash","$","",85000,"",False),
 ("ar","Accounts receivable","$","",160000,"",False),
 ("inventory","Inventory","$","",140000,"",False),
 ("otherCA","Other current assets","$","",15000,"Prepaids, deposits",True),
 ("cl","Current liabilities","$","",230000,"Payables, accruals, current portion of debt, line balance",False),
],
results=[("current","Current ratio","primary"),("quick","Quick ratio",""),("wc","Working capital",""),("ca","Total current assets","")],
formula="Current ratio = Current assets ÷ current liabilities\nQuick ratio = (Cash + receivables) ÷ current liabilities\nWorking capital = Current assets − current liabilities",
template="spread", wfs=True,
related=["cash-conversion-cycle-calculator","dscr-calculator","borrowing-base-calculator"],
guide="""
<h2>What these ratios show</h2>
<p>Liquidity ratios answer a simple question: if every bill due in the next twelve months came due, could the business pay it from assets that turn into cash within the same year?</p>
<ul>
 <li><strong>Current ratio</strong> compares all current assets to current liabilities. 1.50 means $1.50 of short-term assets for every $1.00 of short-term obligations.</li>
 <li><strong>Quick ratio</strong> counts only cash and receivables, leaving out inventory and prepaid expenses, which can take time to convert or can't be converted at all.</li>
 <li><strong>Working capital</strong> is the dollar difference, the cushion the business operates on.</li>
</ul>

<h2>What lenders look for</h2>
<p>Many commercial lenders like a current ratio of at least 1.20 to 1.50 and a quick ratio near 1.00, and some write minimums into loan covenants. Context matters: a distributor carrying heavy inventory will have a much higher current ratio than quick ratio, while a service business may have almost no inventory, so the two ratios are close.</p>

<h2>Common reasons the ratios look weak</h2>
<ol>
 <li><strong>Long-term needs funded with short-term money.</strong> Buying equipment or a vehicle out of the line of credit puts long-lived assets against current debt. Term out the borrowing instead.</li>
 <li><strong>Current portion of long-term debt.</strong> A loan maturing within twelve months moves entirely into current liabilities. Refinance before year end if possible.</li>
 <li><strong>Owner distributions.</strong> Large draws reduce cash directly.</li>
 <li><strong>Slow collections or excess inventory,</strong> which inflate the current ratio while the quick ratio stays weak. Check your <a href="/cash-conversion-cycle-calculator/">cash conversion cycle</a>.</li>
</ol>

<h2>A ratio is a snapshot</h2>
<p>Balance sheet ratios reflect a single day, so they can swing with timing, such as a large customer payment arriving the day after month end. Track them monthly from consistent, reconciled books, and look at the trend rather than one reading.</p>
""",
faqs=[
 ("What is a good current ratio?","Between about 1.20 and 2.00 is generally healthy for small businesses. Below 1.00 means current liabilities exceed current assets."),
 ("What is the difference between the current ratio and the quick ratio?","The quick ratio leaves out inventory and prepaid expenses, counting only cash and receivables, so it is a stricter test of liquidity."),
 ("Can a current ratio be too high?","Yes. A very high ratio can mean cash is sitting idle or inventory and receivables are building up instead of turning into cash."),
 ("Is the line of credit balance a current liability?","Usually, yes. Revolving lines are typically due within a year and are classified as current liabilities."),
]),
]
