# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.25.1",
#     "anywidget==0.11.0",
#     "numpy==2.5.2",
#     "pandas==3.0.5",
#     "matplotlib==3.11.1",
#     "traitlets==5.16.1",
# ]
# ///

# Narrative paragraphs stay on one line; final expressions display marimo outputs.
# ruff: noqa: E501, B018
import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Thresholds And Review Decisions")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    return mo, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Thresholds And Review Decisions

    An anomaly score ranks observations by unusualness. A threshold turns that ranking into a review list: select every record whose score is at least the threshold. Lowering the threshold admits more records. What does that additional review accomplish?

    Here we investigate which chemical profiles are unusual, then compare the flags with **sensory quality at most 4** as an external criterion. Low ratings are a candidate proxy for a problematic wine; they are not established chemical-anomaly labels. The 1,599 red-wine records contain 63 such wines. The ratings come from expert sensory assessments; they were excluded when fitting both detectors. A positive outcome below means a rating at most 4. Measurement errors and production faults would require different outcome evidence.

    **Before moving the slider:** predict what lowering the threshold will do to the number reviewed, the low-rated wines found, and the proportion of reviews that find a low-rated wine.
    """)
    return


@app.cell(hide_code=True)
def _(mo, pd):
    # The fixed scores make threshold changes independent of fitting and randomness.
    records = pd.read_csv(mo.notebook_location() / "evidence-scores.csv")
    assert len(records) == 1599 and records.record.is_unique
    assert records[["LOF", "IF", "quality"]].notna().all().all()
    return (records,)


@app.cell(hide_code=True)
def _(mo):
    method = mo.ui.dropdown(
        options={"Local Outlier Factor": "LOF", "Isolation Forest": "IF"},
        value="Local Outlier Factor",
        label="Detector",
    )
    method
    return (method,)


@app.cell(hide_code=True)
def _():
    import anywidget
    import traitlets

    class ScoreThreshold(anywidget.AnyWidget):
        """A score-axis cutoff with linked record marks; no remote JS dependencies."""

        scores = traitlets.List(traitlets.Float()).tag(sync=True)
        low_quality = traitlets.List(traitlets.Bool()).tag(sync=True)
        boundaries = traitlets.List(traitlets.Float()).tag(sync=True)
        cutoff = traitlets.Float().tag(sync=True)
        _esm = r"""
        export function countsAt(scores, labels, cutoff) {
          let tp = 0, fp = 0, fn = 0, tn = 0;
          scores.forEach((score, i) => {
            if (score >= cutoff) { if (labels[i]) tp++; else fp++; }
            else { if (labels[i]) fn++; else tn++; }
          });
          return {tp, fp, fn, tn};
        }
        export function nearestBoundary(boundaries, score) {
          let lo = 0, hi = boundaries.length - 1;
          while (lo < hi) {
            const mid = Math.floor((lo + hi) / 2);
            if (boundaries[mid] < score) lo = mid + 1; else hi = mid;
          }
          if (lo > 0 && score - boundaries[lo - 1] < boundaries[lo] - score) lo--;
          return lo;
        }
        function render({model, el}) {
          const scores = model.get('scores'), labels = model.get('low_quality');
          const bounds = model.get('boundaries');
          const min = bounds[0], max = bounds[bounds.length - 1];
          const left = 150, right = 870, width = 900;
          const x = s => left + (s - min) / (max - min) * (right - left);
          el.innerHTML = `<div class="score-threshold">
            <p><strong>Drag the boundary, click the plot, or use the slider.</strong><br>
            Each dot is one wine; horizontal position is its anomaly score. Vertical spread separates overlapping dots.</p>
            <svg viewBox="0 0 900 300" role="img" aria-label="Wine scores in two rows with a movable review threshold"></svg>
            <label>Threshold <output></output><input type="range" min="0" max="${bounds.length - 1}" step="1" aria-label="Anomaly score threshold"></label>
            <div class="presets">Review capacity: <button data-budget="25">25</button><button data-budget="50">50</button><button data-budget="100">100</button><button data-budget="${scores.length}">All</button><button data-budget="0">None</button></div>
            <p class="readout" aria-live="polite"></p>
            <small>Score ≥ threshold → flagged. Tied scores move together. Scores measure unusualness, not probability of low quality.</small>
          </div>`;
          const svg = el.querySelector('svg'), slider = el.querySelector('input');
          const ns = 'http://www.w3.org/2000/svg';
          function node(tag, attrs, text) {
            const n = document.createElementNS(ns, tag);
            Object.entries(attrs).forEach(([k,v]) => n.setAttribute(k, v));
            if (text !== undefined) n.textContent = text;
            svg.appendChild(n); return n;
          }
          node('rect', {x:left, y:40, width:right-left, height:195, fill:'#f3f4f6'});
          const shade = node('rect', {y:40, height:195, fill:'#dceef4'});
          node('text', {x:left, y:20, 'font-size':14}, 'Unflagged ←');
          node('text', {x:right, y:20, 'font-size':14, 'text-anchor':'end'}, '→ Flagged for review');
          node('text', {x:12, y:89, 'font-size':14}, 'Quality ≤ 4');
          node('text', {x:12, y:108, 'font-size':12}, '63 wines');
          node('text', {x:12, y:184, 'font-size':14}, 'Quality > 4');
          node('text', {x:12, y:203, 'font-size':12}, '1,536 wines');
          node('line', {x1:left, x2:right, y1:137, y2:137, stroke:'#c7ced5'});
          const dots = scores.map((score, i) => {
            const y = (labels[i] ? 90 : 185) + ((i * 37 % 101) / 100 - .5) * 70;
            const dot = node('circle', {cx:x(score), cy:y, r:labels[i]?3.5:2.7,
              fill:labels[i]?'#aa481e':'#27618e', opacity:labels[i]?.85:.4});
            const title = document.createElementNS(ns, 'title');
            title.textContent = `Record ${i+1}; score ${score.toPrecision(6)}; ${labels[i]?'quality ≤ 4':'quality > 4'}`;
            dot.appendChild(title); return dot;
          });
          node('line', {x1:left, x2:right, y1:240, y2:240, stroke:'#46515f'});
          for (let i=0;i<=5;i++) {
            const value = min + (max-min)*i/5;
            node('text', {x:x(value), y:261, 'font-size':12, 'text-anchor':'middle'}, value.toFixed(2));
          }
          node('text', {x:(left+right)/2, y:289, 'font-size':14, 'text-anchor':'middle'}, 'Anomaly score → more unusual');
          const line = node('line', {y1:35, y2:240, stroke:'#111827', 'stroke-width':3});
          const handle = node('path', {fill:'#111827'});
          let index = nearestBoundary(bounds, model.get('cutoff'));
          function paint() {
            const cutoff = bounds[index], cx = x(cutoff);
            slider.value = index;
            slider.setAttribute('aria-valuetext', cutoff.toPrecision(7));
            el.querySelector('output').textContent = cutoff.toPrecision(7);
            line.setAttribute('x1', cx); line.setAttribute('x2', cx);
            handle.setAttribute('d', `M ${cx-8} 28 L ${cx+8} 28 L ${cx} 40 Z`);
            shade.setAttribute('x', cx); shade.setAttribute('width', Math.max(0,right-cx));
            dots.forEach((dot,i) => dot.setAttribute('stroke', scores[i]>=cutoff?'#172e40':'none'));
            const c = countsAt(scores, labels, cutoff), n = c.tp+c.fp;
            el.querySelector('.readout').textContent = `${n} flagged · TP ${c.tp} · FP ${c.fp} · FN ${c.fn} · TN ${c.tn} · Precision ${n?(100*c.tp/n).toFixed(1)+'%':'undefined'} · Recall ${(100*c.tp/(c.tp+c.fn)).toFixed(1)}%`;
          }
          function commit() { model.set('cutoff', bounds[index]); model.save_changes(); }
          function fromPointer(event) {
            const point = svg.createSVGPoint(); point.x=event.clientX; point.y=event.clientY;
            const position = point.matrixTransform(svg.getScreenCTM().inverse());
            const fraction = Math.max(0,Math.min(1,(position.x-left)/(right-left)));
            index = nearestBoundary(bounds,min+fraction*(max-min)); paint();
          }
          let dragging = false;
          svg.addEventListener('pointerdown', event => {
            dragging=true; svg.setPointerCapture(event.pointerId); fromPointer(event);
          });
          svg.addEventListener('pointermove', event => { if(dragging) fromPointer(event); });
          svg.addEventListener('pointerup', event => {
            if(dragging) { fromPointer(event); dragging=false; commit(); }
          });
          svg.addEventListener('pointercancel', () => { dragging=false; commit(); });
          slider.addEventListener('input', () => { index=Number(slider.value); paint(); });
          slider.addEventListener('change', commit);
          const ordered = [...scores].sort((a,b)=>b-a);
          el.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
            const n = Number(button.dataset.budget);
            index = nearestBoundary(bounds, n===0?max:ordered[n-1]); paint(); commit();
          }));
          function changed() { index=nearestBoundary(bounds,model.get('cutoff')); paint(); }
          model.on('change:cutoff',changed); paint();
          return () => model.off('change:cutoff',changed);
        }
        export default {render};
        """
        _css = """
        .score-threshold {background:#fff;color:#172331;border:1px solid #cbd5df;border-radius:10px;padding:16px;font:14px/1.5 system-ui;}
        .score-threshold svg {width:100%;display:block;touch-action:none;cursor:ew-resize;}
        .score-threshold input {display:block;width:100%;accent-color:#27618e;}
        .score-threshold output {font-variant-numeric:tabular-nums;font-weight:600;margin-left:8px;}
        .score-threshold button {margin:6px 4px;padding:4px 12px;border:1px solid #94a3b8;border-radius:5px;background:#f4f7fa;color:#172331;cursor:pointer;}
        .score-threshold .readout {font-weight:600;font-variant-numeric:tabular-nums;}
        """

    return (ScoreThreshold,)


@app.cell(hide_code=True)
def _(ScoreThreshold, method, mo, np, records):
    scores = records[method.value].to_numpy()
    boundaries = np.append(np.unique(scores), np.nextafter(scores.max(), np.inf))
    visual_threshold = mo.ui.anywidget(
        ScoreThreshold(
            scores=scores.tolist(),
            low_quality=records.quality.le(4).tolist(),
            boundaries=boundaries.tolist(),
            cutoff=float(np.sort(scores)[-50]),
        )
    )
    mo.vstack(
        [
            visual_threshold,
            mo.md(
                "The counts in the graphic update while you drag. Release the boundary to update the detailed results below. Switching detectors resets to the 50th-highest score. Capacity buttons select that ranked score; ties can make the count larger."
            ),
        ]
    )
    return boundaries, scores, visual_threshold


@app.cell(hide_code=True)
def _(visual_threshold):
    from types import SimpleNamespace

    threshold = SimpleNamespace(value=visual_threshold.value["cutoff"])
    return (threshold,)


@app.cell(hide_code=True)
def _(records, scores, threshold):
    # These four counts partition the same collection at every threshold.
    target = records.quality.to_numpy() <= 4
    selected = scores >= threshold.value
    tp = int((selected & target).sum())
    fp = int((selected & ~target).sum())
    fn = int((~selected & target).sum())
    tn = int((~selected & ~target).sum())
    reviewed = tp + fp
    return fn, fp, reviewed, selected, target, tn, tp


@app.cell(hide_code=True)
def _(fn, fp, mo, reviewed, tn, tp):
    _precision = f"{tp} / {reviewed} = {tp / reviewed:.1%}" if reviewed else "undefined (0 reviews)"
    mo.md(f"""
    ## Review Results

    **{reviewed:,} records selected · {tp} low-rated wines found · {fn} low-rated wines missed**

    The rows show the review decision; the columns show the recorded sensory outcome. True and false describe agreement with the low-rating criterion; disagreement does not establish that a chemical anomaly was detected incorrectly.

    | | Quality ≤ 4 | Quality > 4 |
    | :--- | ---: | ---: |
    | **Selected for review** | **{tp}** true positives (TP) | **{fp}** false positives (FP) |
    | **Left unselected** | **{fn}** false negatives (FN) | **{tn}** true negatives (TN) |

    **Precision = TP / (TP + FP) = {_precision}**  
    Among the records selected, what fraction have low ratings?

    **Recall = TP / (TP + FN) = {tp} / {tp + fn} = {tp / (tp + fn):.1%}**  
    Among all low-rated wines, what fraction did the list retrieve?
    """)
    return


@app.cell(hide_code=True)
def _(mo, np, plt, reviewed, scores, target, threshold, tp):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 3.4), layout="constrained")
    _bins = np.linspace(scores.min(), scores.max(), 40)
    for _mask, _label, _color in [
        (~target, "Quality > 4", "#4477aa"),
        (target, "Quality ≤ 4", "#bb5522"),
    ]:
        _axes[0].hist(
            scores[_mask], bins=_bins, histtype="step", linewidth=2, label=_label, color=_color
        )
    _axes[0].axvline(threshold.value, color="black", linestyle="--", label="Threshold")
    _axes[0].set(
        xlabel="Anomaly score (larger = more unusual)",
        ylabel="Records",
        title="Review records at or right of the line",
    )
    _axes[0].legend(fontsize=8)
    _order = np.argsort(-scores, kind="stable")
    _axes[1].step(np.arange(1, len(scores) + 1), np.cumsum(target[_order]), where="post")
    _axes[1].scatter([reviewed], [tp], color="black", zorder=3)
    _axes[1].plot(
        [0, len(scores)],
        [0, int(target.sum())],
        ":",
        color="gray",
        label="Random selection: expected count",
    )
    _axes[1].set(
        xlabel="Records reviewed",
        ylabel="Low-rated wines found",
        title="Current workload and yield",
        xlim=(0, len(scores)),
        ylim=(0, int(target.sum()) + 2),
    )
    _axes[1].legend(fontsize=8)
    mo.vstack(
        [
            mo.as_html(_fig),
            mo.md(
                "The histogram counts records on a shared scale; low-rated wines are rare. The dot on the right shows the current selection. Its curve follows score order; tied records cross the threshold together. The dotted line gives the expected count from uniform random selection, not a measured alternative detector."
            ),
        ]
    )
    plt.close(_fig)
    return


@app.cell(hide_code=True)
def _(mo, np, records, scores, selected, threshold):
    _near = np.argsort(np.abs(scores - threshold.value), kind="stable")[:10]
    _table = records.iloc[_near][["record", "quality"]].copy()
    _table["score"] = scores[_near]
    _table["review"] = np.where(selected[_near], "Selected", "Unselected")
    _table["outcome"] = np.where(_table.quality <= 4, "Quality ≤ 4", "Quality > 4")
    _table = _table.sort_values(["score", "record"], ascending=[False, True])
    mo.vstack(
        [
            mo.md(
                "### Records Near The Threshold\n\nThese ten records have scores closest to the current threshold. Follow their selection status as you move it. Record numbers locate rows in the original file."
            ),
            mo.ui.table(_table, selection=None, show_column_summaries=False),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Try Three Decisions

    1. Start with LOF near 50 reviews. Lower the threshold until about 100 records are selected. How many additional reviews and low-rated wines did you gain?
    2. Move the threshold to select every record, then no records. Explain the precision and recall at each extreme using their denominators.
    3. Switch to Isolation Forest. Compare it with LOF at similar review counts. The methods use different score scales, so equal numerical thresholds do not imply equal workloads.

    A lower threshold cannot reduce the number of target records retrieved. Precision depends on the mix entering the list: additional reviews may bring mostly low-rated wines or mostly other wines. Locate an interval where the review count increases without finding another low-rated wine.

    Choosing a threshold after inspecting these outcomes describes what works on this collection. Evidence about future samples requires a separate evaluation after the policy is fixed. For the original laboratory question about measurements needing correction, we would need recheck outcomes before constructing the corresponding confusion matrix.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Data And Fixed Scores": mo.md("""
        The [UCI Wine Quality data](https://archive.ics.uci.edu/dataset/186/wine+quality), contributed by Cortez and colleagues, are licensed CC BY 4.0. Each row contains chemical measurements and a sensory rating derived from expert evaluations. The criterion quality ≤ 4 is used to investigate agreement with an external outcome.

        The adjacent `evidence-scores.csv` supplies precomputed scores for all 1,599 red-wine records. Both detectors used the same 11 standardized chemical measurements, with quality excluded. LOF used 20 neighbors. Isolation Forest used 300 trees, 256 samples per tree, and seed 7130. Scores were oriented so larger means more unusual. All original rows, including repeated profiles, were retained.

        `verify_foundation.py` reproduces these scores from the original files in `data/`. The slider changes only the cutoff; it never refits a detector. The two methods have separate score scales. Exact score ties stay together under the rule score ≥ threshold.
        """),
        }
    )
    return


if __name__ == "__main__":
    app.run()
