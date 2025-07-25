from collections import deque

class BrowserHistoryDeque:
    def __init__(self, max_size=5):
        self.history = deque(maxlen=max_size)
        self.forward_stack = deque()

    def add_new_page(self, url):
        self.history.append(url)
        self.forward_stack.clear()
        self.print_state()

    def go_back(self):
        if len(self.history) > 1:
            last_page = self.history.pop()
            self.forward_stack.append(last_page)
            print(f"Going back from: {last_page}")
        else:
            print("No pages to go back.")
        self.print_state()

    def go_forward(self):
        if self.forward_stack:
            next_page = self.forward_stack.pop()
            self.history.append(next_page)
            print(f"Going forward to: {next_page}")
        else:
            print("No pages to go forward to.")
        self.print_state()

    def print_state(self):
        print("Current history:", list(self.history))
        print("Forward Stack:", list(self.forward_stack))
        print("-" * 40)

browser = BrowserHistoryDeque()

browser.add_new_page("page1.com")
browser.add_new_page("page2.com")
browser.add_new_page("page3.com")
browser.add_new_page("page4.com")
browser.add_new_page("page5.com")
browser.add_new_page("page6.com")


browser.go_back()
browser.go_back()
browser.go_forward()
browser.add_new_page("page7.com")