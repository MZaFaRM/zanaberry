class Expression:
    def draw_eye(self, surface, x, y, width, height, color):
        """
        Blueprint for drawing an eye.
        Every custom expression will override this method.
        """
        raise NotImplementedError(
            "You must implement draw_eye() in your expression subclass!"
        )
