import plotly.graph_objects as go
from typing import List, Dict, Union, Optional

def make_sankey(
    nodes: List[str],
    links: List[Dict[str, Union[int, str, float]]],
    title: str = "Sankey Diagram",
    *,
    node_pad: int = 15,
    node_thickness: int = 20,
    node_line_color: str = "black",
    node_line_width: float = 0.5,
    font_size: int = 10,
    layout_kwargs: Optional[dict] = None,
):
    """
    Create a Plotly Sankey figure.

    Parameters
    ----------
    nodes : list of str
        Node labels in index order. Index positions are used if a link uses integer sources/targets.
    links : list of dict
        Each dict must contain:
          - 'source' (int or str): Source node index or label
          - 'target' (int or str): Target node index or label
          - 'value'  (float)     : Flow value (must be >= 0)
        Extra keys are ignored.
    title : str, optional
        Figure title.
    node_pad : int, optional
        Pixel padding between nodes.
    node_thickness : int, optional
        Node thickness in pixels.
    node_line_color : str, optional
        Node border color.
    node_line_width : float, optional
        Node border width.
    font_size : int, optional
        Base font size for the figure.
    layout_kwargs : dict, optional
        Extra kwargs forwarded to `fig.update_layout()`.

    Returns
    -------
    plotly.graph_objects.Figure
        A configured Sankey figure (call `.show()` to render).
    """

    # Map labels -> indices for flexible link definitions
    label_to_idx = {label: i for i, label in enumerate(nodes)}

    def _to_index(x):
        if isinstance(x, int):
            return x
        if isinstance(x, str):
            if x not in label_to_idx:
                raise ValueError(f"Node label '{x}' not found in nodes list.")
            return label_to_idx[x]
        raise TypeError(f"Link endpoints must be int or str, got {type(x)}")

    # Build validated sources/targets/values
    sources, targets, values = [], [], []
    for i, link in enumerate(links):
        try:
            s = _to_index(link["source"])
            t = _to_index(link["target"])
            v = float(link["value"])
        except KeyError as e:
            raise KeyError(f"Link {i} missing required key: {e}") from e

        if not (0 <= s < len(nodes)) or not (0 <= t < len(nodes)):
            raise IndexError(f"Link {i} uses out-of-range index: source={s}, target={t}")
        if v < 0:
            raise ValueError(f"Link {i} has negative value: {v}")

        sources.append(s)
        targets.append(t)
        values.append(v)

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=node_pad,
            thickness=node_thickness,
            line=dict(color=node_line_color, width=node_line_width),
            label=nodes
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    ))

    # Apply layout
    fig.update_layout(title_text=title, font_size=font_size)
    if layout_kwargs:
        fig.update_layout(**layout_kwargs)

    return fig

# --- Usage (example placeholders, leave commented for publication) ---
# nodes = ["n studies", "yes", "no", "example1", "example2", "example3",
#          "method1", "method2", "method3", "validation_yes", "validation_no"]
# links = [
#     {"source": "n studies", "target": "yes", "value": 0},
#     {"source": "n studies", "target": "no", "value": 0},
#     # ...
# ]
# fig = make_sankey(nodes, links, title="Sankey Diagram of n Studies")
# fig.show()
