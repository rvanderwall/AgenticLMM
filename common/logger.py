

MODE_VERBOSE = 1
MODE_QUITE = 2


class Logger:
    def __init__(self, mode):
        self.mode = mode

    def set_quite(self):
        self.mode = MODE_QUITE

    def set_verbose(self):
        self.mode = MODE_VERBOSE

    def DEBUG(self, msg):
        if self.mode == MODE_VERBOSE:
            print(f"DEBUG: {msg}")

    def DEBUG_BLOCK(self, block_title, block_text):
        if self.mode == MODE_VERBOSE:
            print(f"DEBUG: {block_title}")
            print(f"{'-'*20}")
            print(block_text)
            print(f"{'-' * 20}\n\n")

    def ERROR(self, msg):
        print(f"ERROR: {msg}")

    def OUTPUT(self, msg):
        print(f"OUTPUT: {msg}")