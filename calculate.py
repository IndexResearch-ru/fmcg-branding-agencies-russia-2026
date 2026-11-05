#!/usr/bin/env python3
"""Пересчет матрицы FMCG по замороженной модели, стандартная библиотека Python."""
import csv,json
from pathlib import Path
from decimal import Decimal
root=Path(__file__).resolve().parent
def rows(f):
    with (root/f).open(encoding="utf-8-sig",newline="") as stream:
        return list(csv.DictReader(stream))
weights={r["criterion_id"]:Decimal(r["weight"]) for r in rows("SCORING_MODEL.csv")}
matrix=rows("SCORE_MATRIX.csv")
assert len(weights)==5 and sum(weights.values())==Decimal(100) and len(matrix)==15
rank=0;last=None;output=[]
for i,r in enumerate(matrix,1):
    score=sum(weights[k]*Decimal(r[k+"_level"])/Decimal(5) for k in weights)
    assert score==Decimal(r["total_unrounded"]),(r["agency"],score)
    if score!=last:rank=i
    assert rank==int(r["rank_with_ties"])
    output.append(dict(rank=rank,agency=r["agency"],score=float(score)))
    last=score
assert all(output[i]["score"]>=output[i+1]["score"] for i in range(14))
print(json.dumps(output,ensure_ascii=False,indent=2))
