# Adapting SmartBOQ AI for Ukraine

Status: draft. Based on reading README.md, PROJECT_SUMMARY.md,
ai-engine/quantity_calculator.py, ai-engine/cost_estimator.py and
ai-engine/ai_analyzer.py. The frontend and backend are not reviewed yet.

## 1. What the project does today

- ai_analyzer.py sends a drawing (or text extracted from a PDF) to
  OpenAI GPT-4o and gets back a list of elements with dimensions
  (columns, beams, slabs, walls, doors, windows).
- quantity_calculator.py computes quantities with simple geometry
  (concrete, rebar, formwork, bricks, mortar).
- cost_estimator.py multiplies quantities by unit rates and adds
  regional, project-type and inflation factors, plus contingency,
  overhead and profit.
- Target users: professional contractors and developers (Pakistan first).

## 2. Proposal: a calculator for private customers (new idea)

Note: this is my proposal for a different audience. It is not part of
the current project.

The problem: a person who wants to build something (for example, a
summer kitchen on an existing foundation) does not know whether the
project is affordable. Calling a crew just to hear a price costs time,
and without any reference number it is hard to tell whether a quote is
fair or inflated.

The idea: the person opens a website, enters the size of the building,
what already exists (for example, the foundation), the number of
fixtures (sink, sockets, lights) and a budget level (minimum / medium /
maximum). The site returns a price range (for example, "10-15 thousand
USD" as an illustration only) with a breakdown by stage (rough work,
wiring, plumbing, plaster, ceilings, finishing).

What this gives the customer:
- A quick answer to "should I go ahead and hire a crew or not".
- A reference point, so it is easier to notice an inflated quote.
- A clear view of what the price consists of (materials vs. labor).

Principles:
- This is a preliminary estimate, not a formal cost estimate. The note
  must be clearly visible.
- Code calculates, AI only understands the text description. The
  existing structure already works this way: AI produces the list of
  elements, and separate code calculates quantities and costs. For
  private customers, AI would turn a sentence like "kitchen 3x2,
  stretch ceiling, tiles" into the same fields the person would fill
  in a form. No drawings are needed.
- Prices live in a table that is updated manually at first.
- Labor is a percentage of materials (different per stage, shown as a
  range), to be refined after talking to real crews.

## 3. What needs to change

1. Add a form for manual input. Today the input comes from drawings.
2. Add finishing works. The current calculator has no tiles, plaster,
   ceilings, wiring or plumbing. Unknown elements fall back to a
   generic "count" item.
3. Add Ukraine to the rates database with prices in UAH, and add
   city factors (for example Kyiv vs. other regions).
4. Move prices out of the Python code into a separate file (CSV or
   JSON) so they can be updated without touching formulas. Keep a
   "source" and a date for every price.
5. Show a price range (low / high) instead of one number.
6. Do not invent a price when a rate is missing. The current code uses
   a default rate for unknown materials. For customers it is better to
   show "price not set".
7. Replace hard-coded brick values (55 / 110 / 165 per m2). They match
   one brick size and must be recalculated for common Ukrainian bricks.
8. Check rebar and other construction values against Ukrainian norms
   (DBN). Current options are IBC, Eurocode and IS only.
9. Labor: calculate it as a percentage of materials, with a different
   percentage per stage and a low/high range. The labor_ratio field
   already exists in the code but is not used.
10. Replace hard-coded exchange rates (they are based on PKR).

## 3a. Government customers and Prozorro

My assessment: I suggest not focusing on government customers and the
Prozorro tender system. Reasons:

- Competition is high, and the market is occupied by larger, more
  established companies with experience and resources.
- Government work requires estimates in the official format
  (DBN-based estimates, forms such as KB-2v and KB-3), usually made in
  specialized software (for example AVK). A new tool would have to
  match these formats.
- Formal procedures make the first sales slow for a small product.

Private customers and small crews have fewer formal requirements and
can be reached directly, so the focus is on the private market. Tenders
can be reconsidered later.

## 4. Open questions for Ahmed

- Does the project actually calculate prices today, or is it mostly a
  prototype?
- README says Claude, but ai_analyzer.py uses OpenAI GPT-4o. Is the
  README outdated?
- README mentions a cost-database folder, but it is not in the repo.
  Where do rates live?
- For PDFs with text, ai_analyzer.py asks the AI for a "type" field and
  dimensions in millimeters, while quantity_calculator.py expects
  "element_type" and meters. Is this mismatch known?
- Is it OK to add the Ukraine version in my fork and send a pull
  request?