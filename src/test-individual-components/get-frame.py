def get_frame(self, stream_name: str) -> tp.Optional[tp.Any]:
        """
        Get the current frame from a specific video stream.

        Args:
            stream_name (str): The name of the stream to get the frame from.

        Returns:
            The most recent video frame or None if the stream is not available.
        """
        with self.lock:
            if stream_name in self.streams:
                return self.streams[stream_name].get_current_frame()
            else:
                logger.error(f"Stream {stream_name} does not exist.")
                return None