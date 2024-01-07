class ContractAction:
    def __init__(self) -> None:
        self.highlight_to_red = []
        self.highlight_white_to_green = []
        self.highlight_red_to_green = []

        # list of (start, end, u_index)
        # u_index=0 if start=u; u_index=1 if end=u
        self.edge_shrink = []

        # list of (before:start, before:end, after:start, after:end)
        self.edge_move = []
        self.edge_fadeout = []

    def __repr__(self) -> str:
        return '\n'.join([
            f'highlight_to_red        : {self.highlight_to_red}',
            f'highlight_white_to_green: {self.highlight_white_to_green}',
            f'highlight_red_to_green  : {self.highlight_red_to_green}',
            f'edge_shrink             : {self.edge_shrink}',
            f'edge_move               : {self.edge_move}',
            f'edge_fadeout            : {self.edge_fadeout}',
        ])
