# Routing policy (self-contained: use only this file)
Effort scale, lowest to highest: low < medium < high < max.
| model       | family    | cli | lanes                      | floor  | ceiling |
|-------------|-----------|-----|----------------------------|--------|---------|
| atlas-pro   | Northwind | nw  | implement, review, research | high   | max     |
| atlas-lite  | Northwind | nw  | extract, prose             | low    | high    |
| corvid-9    | Corvid    | cv  | implement, review          | medium | max     |
| corvid-mini | Corvid    | cv  | extract                    | low    | medium  |
| pellet-2    | Pellet    | pl  | prose, research            | medium | high    |
Lane order (first eligible model wins):
- implement: atlas-pro, corvid-9
- review: corvid-9, atlas-pro
- research: atlas-pro, pellet-2
- extract: corvid-mini, atlas-lite
- prose: pellet-2, atlas-lite
R1 A model is eligible only if the lane appears in its lanes column.
R2 Reviewer rule: for a review lane, the model's family must differ from the request's author_family.
R3 Pinned CLI: if a request pins a cli, only models on that cli are eligible.
R4 Unavailable: skip any model the request lists as unavailable.
R5 Unrouted: if no model is eligible, answer model "Unrouted" and effort null.
R6 Effort: below the chosen model's floor -> use the floor; above its ceiling -> use the ceiling;
   otherwise keep the requested effort. Effort never makes a model ineligible.
Answer format: answers.json = [{"id": "...", "model": "...", "effort": "..." or null}, ...]
