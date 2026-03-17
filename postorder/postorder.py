from manim import *

# --- Configuration & Palette ---
# A coherent color palette (Nord-inspired) for a professional look
COLOR_BG = "#2E3440"
COLOR_NODE = "#4C566A"
COLOR_NODE_Border = "#81A1C1"
COLOR_ACTIVE = "#EBCB8B"  # Yellow for current processing
COLOR_VISITED = "#A3BE8C"  # Green for finished
COLOR_EDGE = "#D8DEE9"
COLOR_TRACKER = "#BF616A"  # Red/Pink for the execution pointer


class TreeNode(VGroup):
    """A professional node class that handles its own geometry"""

    def __init__(self, value, position, r=0.35):
        super().__init__()
        self.value = value
        self.center_pos = position

        # visual elements
        self.circle = Circle(radius=r, color=COLOR_NODE_Border, fill_color=COLOR_NODE, fill_opacity=1)
        self.circle.set_stroke(width=3)
        self.text = Text(str(value), font="Sans-Serif", font_size=20, color=WHITE)

        self.circle.move_to(position)
        self.text.move_to(position)

        self.add(self.circle, self.text)

        # Graph connections
        self.left = None
        self.right = None
        self.parent = None
        self.edge_to_parent = None


class PostorderTraversal(Scene):
    def construct(self):
        self.camera.background_color = COLOR_BG

        # 1. Setup Layout
        self.setup_header()
        self.setup_code_block()

        # Initialize output values list
        self.output_values = []
        self.setup_output_area()
        self.setup_stack_visualizer()

        # 2. Create Tree (Automated Layout)
        # Tree Data: (Value, Left_Child_Data, Right_Child_Data)
        tree_data = ("1",
                     ("2",
                      ("3", None, None),
                      ("4", None, None)),
                     ("5",
                      ("6", None, None),
                      ("7", None, None))
                     )

        # Position tree higher up to make room for output below
        root = self.build_tree(tree_data, position=UP * 2.5, width=5.0, layer_height=1.2)
        self.draw_tree_edges(root)
        self.bring_to_front(root)  # Ensure nodes are on top of edges

        # 3. Animation Sequence
        self.execution_tracker = Dot(color=COLOR_TRACKER, radius=0.15).move_to(root.center_pos + UP * 0.8)
        self.add(self.execution_tracker)

        self.wait(1)
        self.traverse(root)

        # 4. Final Polish
        self.finish_scene()

    def setup_header(self):
        title = Text("Postorder Traversal", font_size=36, weight=BOLD).to_edge(UP, buff=0.1)
        subtitle = Text("Depth First Search: Left → Right → Root", font_size=20, color=GRAY).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Write(subtitle))

    def setup_code_block(self):
        code_str = """def postorder(node):
    if node is None: 
        return
    postorder(node.left)
    postorder(node.right)
    visit(node)"""

        # Create code using simpler approach without Code class
        self.code_lines = VGroup()
        lines = code_str.split('\n')
        for i, line in enumerate(lines):
            text = Text(line, font="Monospace", font_size=16, color=WHITE)
            text.align_on_border(LEFT, buff=0.2)
            if i == 0:
                text.to_corner(UR, buff=0.5).shift(DOWN * 0.5)
            else:
                text.next_to(self.code_lines[-1], DOWN, aligned_edge=LEFT)
            self.code_lines.add(text)

        # Add background
        code_bg = SurroundingRectangle(
            self.code_lines,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            stroke_width=2
        )
        self.code_group = VGroup(code_bg, self.code_lines)
        self.add(self.code_group)

        # Line highlighter
        self.highlighter = SurroundingRectangle(
            self.code_lines[0],
            color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.1
        )
        # Set initial visibility to hidden
        self.highlighter.set_fill(opacity=0).set_stroke(opacity=0)
        self.add(self.highlighter)

    def setup_output_area(self):
        # Place output at the bottom center of the screen
        self.output_label = Text("Output Sequence: ", font_size=24, color=GRAY)
        self.output_label.to_edge(DOWN, buff=0.8).shift(UP * 0.7 + LEFT * 4.0)

        # Create initial output text (empty)
        self.output_text = Text("", font_size=28, color=COLOR_ACTIVE)
        self.output_text.next_to(self.output_label, RIGHT, buff=0.2)

        # Store the position where output should start
        self.output_position = self.output_label.get_right() + RIGHT * 2.0

        self.add(self.output_label, self.output_text)

    def setup_stack_visualizer(self):
        # A visual representation of the Call Stack
        stack_label = Text("Call Stack", font_size=20, color=GRAY)
        stack_label.next_to(self.code_group, DOWN, buff=0.5)
        self.stack_box = VGroup()
        self.stack_anchor = stack_label.get_bottom() + DOWN * 0.4
        self.add(stack_label)
        self.current_stack = []  # List of VGroups

    def highlight_line(self, line_num):
        # Animate the highlighter moving to the correct code line
        target = self.code_lines[line_num]

        # Check if highlighter is hidden (fill opacity is 0)
        if self.highlighter.get_fill_opacity() == 0:
            self.highlighter.move_to(target)
            self.highlighter.match_width(target)
            self.highlighter.match_height(target, stretch=True)
            self.play(
                self.highlighter.animate.set_fill(opacity=0.1).set_stroke(opacity=1),
                run_time=0.2
            )
        else:
            new_highlighter = SurroundingRectangle(
                target,
                color=YELLOW,
                stroke_width=2,
                fill_color=YELLOW,
                fill_opacity=0.1
            )
            self.play(Transform(self.highlighter, new_highlighter), run_time=0.2)

    def build_tree(self, data, position, width, layer_height):
        """Recursively builds tree nodes with calculated positions"""
        if not data:
            return None

        val, left_data, right_data = data
        node = TreeNode(val, position)
        self.play(FadeIn(node, scale=0.8), run_time=0.3)

        # Calculate children positions
        if left_data:
            left_pos = position + DOWN * layer_height + LEFT * (width / 2)
            node.left = self.build_tree(left_data, left_pos, width / 2, layer_height)
            if node.left:
                node.left.parent = node

        if right_data:
            right_pos = position + DOWN * layer_height + RIGHT * (width / 2)
            node.right = self.build_tree(right_data, right_pos, width / 2, layer_height)
            if node.right:
                node.right.parent = node

        return node

    def draw_tree_edges(self, node):
        if not node:
            return

        if node.left:
            edge = Line(
                node.center_pos + DOWN * 0.2 + LEFT * 0.2,
                node.left.center_pos + UP * 0.2,
                color=COLOR_EDGE,
                stroke_width=4
            )
            edge.z_index = -1
            self.play(Create(edge), run_time=0.2)
            node.left.edge_to_parent = edge
            self.draw_tree_edges(node.left)

        if node.right:
            edge = Line(
                node.center_pos + DOWN * 0.2 + RIGHT * 0.2,
                node.right.center_pos + UP * 0.2,
                color=COLOR_EDGE,
                stroke_width=4
            )
            edge.z_index = -1
            self.play(Create(edge), run_time=0.2)
            node.right.edge_to_parent = edge
            self.draw_tree_edges(node.right)

    def update_stack_display(self, op, value):
        """Adds or removes items from the visual stack"""
        if op == "push":
            txt = Text(f"post({value})", font_size=18, color=COLOR_ACTIVE)
            box = Rectangle(
                height=0.4,
                width=1.5,
                color=COLOR_ACTIVE,
                stroke_width=1,
                fill_color=BLACK,
                fill_opacity=0.8
            )
            item = VGroup(box, txt)

            # Position logic
            if not self.current_stack:
                item.move_to(self.stack_anchor)
            else:
                item.next_to(self.current_stack[-1], DOWN, buff=0.05, aligned_edge=LEFT)

            self.current_stack.append(item)
            self.play(FadeIn(item, shift=UP * 0.1), run_time=0.3)

        elif op == "pop":
            if self.current_stack:
                item = self.current_stack.pop()
                self.play(FadeOut(item, shift=DOWN * 0.1), run_time=0.3)

    def update_output(self, value):
        """Update the output sequence with commas"""
        self.output_values.append(value)

        # Create the comma-separated sequence
        if len(self.output_values) == 1:
            sequence = value
        else:
            sequence = ", ".join(self.output_values)

        # Create new text with the updated sequence
        new_output = Text(sequence, font_size=28, color=COLOR_ACTIVE)
        new_output.move_to(self.output_position)

        # Transform the old text to the new one
        self.play(Transform(self.output_text, new_output), run_time=0.3)

    def traverse(self, node):
        if node is None:
            # Highlight base case check
            self.highlight_line(1)
            self.wait(0.3)
            return

        # 1. PUSH TO STACK
        self.update_stack_display("push", node.value)

        # 2. Move Tracker to Node (but don't visit yet)
        self.play(
            self.execution_tracker.animate.move_to(node.center_pos + UP * 0.6),
            node.circle.animate.set_stroke(color=COLOR_ACTIVE, width=5),
            run_time=0.5
        )

        # 3. RECURSE LEFT (First)
        self.highlight_line(2)
        if node.left:
            # Animate travel down edge
            self.play(
                ShowPassingFlash(
                    node.left.edge_to_parent.copy().set_color(COLOR_ACTIVE),
                    time_width=0.5
                ),
                run_time=0.5
            )
            self.traverse(node.left)
            # Animate return up edge (backtracking)
            self.play(
                self.execution_tracker.animate.move_to(node.center_pos + UP * 0.6),
                run_time=0.5
            )
            self.highlight_line(2)  # Show we returned to this line

        # 4. RECURSE RIGHT (After left)
        self.highlight_line(3)
        if node.right:
            # Animate travel down edge
            self.play(
                ShowPassingFlash(
                    node.right.edge_to_parent.copy().set_color(COLOR_ACTIVE),
                    time_width=0.5
                ),
                run_time=0.5
            )
            self.traverse(node.right)
            # Animate return up edge
            self.play(
                self.execution_tracker.animate.move_to(node.center_pos + UP * 0.6),
                run_time=0.5
            )
            self.highlight_line(3)  # Show we returned to this line

        # 5. VISIT NODE (After both children)
        self.highlight_line(4)

        # Flash node and update output
        self.update_output(node.value)

        # Animate the node being visited
        self.play(
            node.circle.animate.set_fill(COLOR_ACTIVE),
            node.text.animate.set_color(BLACK),
            run_time=0.3
        )
        self.play(
            node.circle.animate.set_fill(COLOR_VISITED, opacity=1).set_stroke(color=COLOR_VISITED),
            node.text.animate.set_color(WHITE),
            run_time=0.2
        )

        # 6. POP STACK (Function finish)
        self.update_stack_display("pop", node.value)

    def finish_scene(self):
        # Hide the highlighter
        self.play(
            self.highlighter.animate.set_fill(opacity=0).set_stroke(opacity=0),
            run_time=0.5
        )

        # Fade out the execution tracker
        self.play(
            self.execution_tracker.animate.scale(1.5).set_opacity(0),
            run_time=1
        )

        # Highlight final output
        output_bg = SurroundingRectangle(
            VGroup(self.output_label, self.output_text),
            color=GREEN,
            buff=0.2,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.3
        )
        self.play(Create(output_bg))

        # Add final summary
        final_text = Text(
            "Postorder Traversal",
            font_size=24,
            color=GREEN
        )
        final_text.next_to(output_bg, UP, buff=0.3)
        self.play(Write(final_text))

        self.wait(3)