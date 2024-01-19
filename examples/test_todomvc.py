from parameterized import parameterized
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class TodoMVC(BaseCase):
    @parameterized.expand([["jquery"], ["react"], ["vue"]])
    def test_todomvc(self, framework):
        self.open("https://todomvc.com/")
        self.clear_local_storage()
        self.click('a[href*="examples/%s/dist"]' % framework)
        self.assert_element("section.todoapp")
        self.assert_text("todos", "header h1")
        self.wait_for_ready_state_complete()
        title = self.get_title()
        self.assert_in(framework, title.lower())
        new_todo_input = "input.new-todo"
        todo_count_span = "span.todo-count"
        self.wait_for_ready_state_complete()
        self.type(new_todo_input, "Learn Python\n")
        self.type(new_todo_input, "Learn JavaScript\n")
        self.type(new_todo_input, "Learn SeleniumBase\n")
        self.assert_text("3 items left", todo_count_span)
        self.check_if_unchecked("ul.todo-list li input")
        self.check_if_unchecked("ul.todo-list li:nth-of-type(2) input")
        self.check_if_unchecked("ul.todo-list li:nth-of-type(3) input")
        self.assert_text("0 items left", todo_count_span)
        self.click("button.clear-completed")
        self.assert_element_not_visible(todo_count_span)
