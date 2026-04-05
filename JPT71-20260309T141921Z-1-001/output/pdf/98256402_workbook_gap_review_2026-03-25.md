# 98256402 Invoice vs JPT-reconciled_v6.0 Review

Date: 2026-03-25

## Scope

- PDF reviewed: `98256402.pdf`
- Workbook reviewed: `JPT71_Dashboard_Final_Email_Pack_2026-03-10/JPT-reconciled_v6.0.xlsx`

## Extracted invoice facts

- Invoice number: `98256402`
- Invoice date: `2026-03-24`
- Due date: `2026-04-22`
- Customer: `SAMSUNG C & T CORPORATION - ABU DHABI`
- Contract number: `OLCOF24-ALS086`
- Service: JOPETWIL 71 charter hire for `2026-02-01` to `2026-02-28`
- Quantity: `28` days
- Unit price: `USD 12,000/day`
- Total before/after tax: `USD 336,000`
- Company-code amount: `AED 1,233,960`
- VAT: `0`
- Exchange rate shown on invoice: `3.6725`

## Workbook findings

- `98256402` does not exist in the reviewed workbook.
- `11_ALS_Allocation` currently includes ALS invoice `98256356` for supply month `2026-01`, but no ALS invoice for `2026-02`.
- `8_Decklog_Context` includes placeholder context `JPT71 202602` for:
  - `2026-01` with 2 rows
  - `2026-02` with 27 rows
  - `2026-03` with 8 rows
- `3_Voyage_Master` contains no `2026-02` loading rows in the reviewed workbook/source workbook.

## Consistency check against existing ALS pattern

- Existing ALS invoice `98256356` in `11_ALS_Allocation` sums to `AED 1,366,170.02`.
- That equals `USD 372,000.01` at `3.6725`, effectively `USD 12,000/day` for 31 days.
- Therefore invoice `98256402` is consistent with the workbook's latest ALS allocation pattern.

## Gap assessment

- I infer the packaged workbook was frozen before ALS issued invoice `98256402`.
- Reason:
  - workbook pack date is `2026-03-10`
  - PDF creation/invoice date is `2026-03-24`
  - ALS allocation stops at `2026-01`

## Why workbook update cannot be completed from current inputs alone

- The workbook has February 2026 decklog context, but no February 2026 voyage master rows.
- Without voyage-level February tonnage/loading data, `11_ALS_Allocation` cannot be recomputed on the same ton-weighted basis used for prior ALS invoices.
- As a result, `12_Cost_Summary` and any dashboard payload derived from ALS allocations also cannot be updated reliably from only this PDF plus the packaged workbook.

## Secondary document conflict to reconcile

- `JOPETWIL71_Legal_Risk_Assessment_20260311.md` states a charter hire rate of `USD 10,000/day`.
- The workbook's latest ALS allocation (`98256356`) and the new invoice (`98256402`) both align with `USD 12,000/day`.
- This should be treated as a document inconsistency until the governing amendment/supporting invoice trail is confirmed.

## Recommended next inputs

1. February 2026 voyage master rows with `Voyage No`, `Loading Date`, and `Delivery Qty`.
2. The source used to build ALS allocations after January 2026, if separate from `VOYAGE`.
3. The governing amendment or approval that changed the effective charter rate to `USD 12,000/day`, if that rate change is intended.
