import gradio as gr


def create_interface(trials):
    buttons = []
    for i, trial in enumerate(trials):
        for j, problem in enumerate(trial):
            color = "green" if problem == 1 else "red"
            buttons.append(
                gr.inputs.Button(label=f"Problem {j+1} of Trial {i+1}", color=color)
            )
    return buttons


iface = gr.Interface(fn=create_interface, inputs="list", outputs="list")
iface.launch()
