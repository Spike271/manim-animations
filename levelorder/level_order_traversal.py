from manim import *
import collections


class LevelOrderTraversal(Scene):
    def construct(self):
        # -----------------------------------------
        # 1. SETUP DATA
        # -----------------------------------------
        adj_list = {
            1: [2, 3],
            2: [4, 5],
            3: [6, 7],
            4: [], 5: [], 6: [], 7: []
        }

        node_positions = {
            1: [0, 2.5, 0],
            2: [-2.5, 0.5, 0],
            3: [2.5, 0.5, 0],
            4: [-3.5, -1.5, 0],
            5: [-1.5, -1.5, 0],
            6: [1.5, -1.5, 0],
            7: [3.5, -1.5, 0],
        }

        # -----------------------------------------
        # 2. CREATE OBJECTS
        # -----------------------------------------

        # Create Edge Mobjects (Lines) - FIXED
        edge_group = VGroup()
        for parent, children in adj_list.items():
            for child in children:
                start_pos = node_positions[parent]
                end_pos = node_positions[child]
                # Simple Line without updaters
                line = Line(start_pos, end_pos, color=GRAY, stroke_width=4)
                edge_group.add(line)

        # Create Node Mobjects
        nodes_map = {}
        node_group = VGroup()

        for val, pos in node_positions.items():
            # Fill black so the line behind it is hidden
            circle = Circle(radius=0.4, color=WHITE, fill_color=BLACK, fill_opacity=1).move_to(pos)
            label = Text(str(val), font_size=24).move_to(pos)
            node_obj = VGroup(circle, label)
            nodes_map[val] = node_obj
            node_group.add(node_obj)

        # UI Text
        title = Text("Level Order Traversal (BFS)", font_size=36).to_edge(UP)
        queue_label = Text("Queue: ", font_size=24, color=YELLOW).to_corner(DL).shift(UP * 1.5)
        queue_content_text = Text("[]", font_size=24).next_to(queue_label, RIGHT)
        output_label = Text("Output: ", font_size=24, color=GREEN).next_to(queue_label, DOWN, buff=0.5)
        output_content_text = Text("", font_size=24).next_to(output_label, RIGHT)

        # -----------------------------------------
        # 3. INITIAL ANIMATION
        # -----------------------------------------
        self.play(Write(title))

        # 1. Draw Lines first
        self.play(Create(edge_group), run_time=1.5)
        # 2. Draw Nodes on top of lines
        self.play(FadeIn(node_group))

        self.play(Write(queue_label), Write(queue_content_text),
                  Write(output_label), Write(output_content_text))
        self.wait(1)

        # -----------------------------------------
        # 4. BFS ANIMATION LOGIC
        # -----------------------------------------
        queue = collections.deque([1])
        visited_output = []

        def update_queue_visual(q):
            content = str(list(q))
            new_text = Text(content, font_size=24).next_to(queue_label, RIGHT)
            return Transform(queue_content_text, new_text)

        def update_output_visual(out):
            content = ", ".join(map(str, out))
            new_text = Text(content, font_size=24).next_to(output_label, RIGHT)
            return Transform(output_content_text, new_text)

        self.play(update_queue_visual(queue))

        while queue:
            curr_val = queue.popleft()
            curr_node_obj = nodes_map[curr_val]
            circle = curr_node_obj[0]

            # Highlight processing (Blue)
            self.play(
                circle.animate.set_fill(BLUE, opacity=0.8).set_stroke(BLUE),
                update_queue_visual(queue),
                run_time=0.6
            )

            visited_output.append(curr_val)
            self.play(update_output_visual(visited_output), run_time=0.4)

            children = adj_list.get(curr_val, [])
            if children:
                for child in children:
                    queue.append(child)
                    # Flash the edge to the child to show discovery
                    child_pos = node_positions[child]
                    parent_pos = node_positions[curr_val]
                    temp_line = Line(parent_pos, child_pos, color=YELLOW, stroke_width=6)
                    self.play(Create(temp_line), run_time=0.3)
                    self.play(FadeOut(temp_line), run_time=0.2)

                self.play(update_queue_visual(queue), run_time=0.5)

            # Mark processed (Green)
            self.play(
                circle.animate.set_fill(GREEN, opacity=0.5).set_stroke(GREEN),
                run_time=0.3
            )

        self.wait(2)