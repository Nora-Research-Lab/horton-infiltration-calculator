import gradio as gr
import numpy as np
import tempfile
import os
from horton_infiltration_calculator import compute_horton

def run_horton(f0, fc, k, t_start, t_end, dt):
    try:
        result = compute_horton(f0, fc, k, t_start, t_end, dt)
    except ValueError as e:
        return (
            gr.Dataframe(value=None, visible=False),
            gr.Plot(value=None),
            f"Error: {e}",
            None
        )
    except Exception as e:
        return (
            gr.Dataframe(value=None, visible=False),
            gr.Plot(value=None),
            f"Unexpected error: {e}",
            None
        )

    t = result["t"]
    f_t = result["f_t"]
    F_t = result["F_t"]

    # build table
    table_data = np.column_stack((t, f_t, F_t))
    headers = ["t (hr)", "f(t) (mm/hr)", "F(t) (mm)"]
    df = gr.Dataframe(value=table_data, headers=headers, label="Infiltration Table", interactive=False)

    # build plot
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.plot(t, f_t, 'b-', label='Infiltration rate f(t)')
    ax1.axhline(y=result["fc"], color='gray', linestyle='--', alpha=0.7, label=f'f_c = {result["fc"]:.1f} mm/hr')
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Infiltration rate (mm/hr)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.legend(loc='upper right')

    ax2 = ax1.twinx()
    ax2.plot(t, F_t, 'g-', label='Cumulative infiltration F(t)')
    ax2.set_ylabel('Cumulative infiltration (mm)', color='g')
    ax2.tick_params(axis='y', labelcolor='g')
    ax2.legend(loc='upper left')

    fig.tight_layout()
    plt.close(fig)  # prevent duplicate display

    # summary
    total_inf = result["F_total"]
    steady_time = result["time_to_steady"]
    if steady_time is not None:
        summary_text = f"Total infiltration (final F): {total_inf:.2f} mm\nTime to reach near‑steady state (within 5% of fc): {steady_time:.3f} hr"
    else:
        summary_text = f"Total infiltration (final F): {total_inf:.2f} mm\nSteady state not reached in the given time range."

    # CSV file for download button
    csv_path = tempfile.mktemp(suffix='.csv')
    np.savetxt(csv_path, table_data, delimiter=",", header=",".join(headers), comments='')
    csv_file = gr.File(value=csv_path, visible=False)

    return df, fig, summary_text, csv_file

with gr.Blocks(title="Horton Infiltration Calculator") as demo:
    gr.Markdown("# Horton Infiltration Calculator")
    with gr.Row():
        f0 = gr.Number(label="Initial infiltration rate f₀ (mm/hr)", value=100.0)
        fc = gr.Number(label="Steady infiltration rate f_c (mm/hr)", value=20.0)
        k = gr.Number(label="Decay constant k (1/hr)", value=2.0)
    with gr.Row():
        t_start = gr.Number(label="Time start t_start (hr)", value=0.0)
        t_end = gr.Number(label="Time end t_end (hr)", value=5.0)
        dt = gr.Number(label="Time step Δt (hr)", value=0.1)
    with gr.Row():
        compute_btn = gr.Button("Compute", variant="primary")
        # download button uses a separate button; we'll link it via state
    table = gr.Dataframe(label="Infiltration Table", interactive=False)
    plot = gr.Plot(label="Infiltration vs Time")
    summary = gr.Textbox(label="Summary", lines=3, interactive=False)
    # hidden file output for download button
    csv_file_out = gr.File(label="Download CSV", visible=False)

    # when compute is clicked, update all outputs
    compute_btn.click(
        fn=run_horton,
        inputs=[f0, fc, k, t_start, t_end, dt],
        outputs=[table, plot, summary, csv_file_out]
    )
    # additional download button that triggers the same function? 
    # Better: after compute, show the CSV file output; but spec wants a download button.
    # We'll add a separate button that, when clicked, triggers the compute again and returns CSV.
    # To avoid recomputing, we can store the latest result in a state variable.
    # Simpler: use gr.DownloadButton if available; for compatibility, we'll implement as:
    # A button that runs a separate function that uses state? For simplicity, we'll just recompute.
    # But the user may want to download without recomputing. We'll store the computed dataframe in a state.
    # Use gr.State to hold the table data. Then download button reads from state.
    # Implement state:
    state = gr.State()
    def store_and_output(*args):
        result = run_horton(*args)
        state.update(result[0].value if result[0] is not None else None)
        return result
    # We'll redefine the click to use store_and_output, and then add a download button that reads from state.
    # However, that's getting complicated. For the spec, the download button can be the file output itself, 
    # as a clickable link. The file output is not a button but a file component that users can click to download.
    # That fulfills "Download button for table as CSV". We can make the file output visible and label it as a button.
    # Actually, gr.File with interactive=False still shows a clickable file that can be downloaded. 
    # So we can simply make the file output visible after computation.
    # We'll modify run_horton to return the file and set csv_file_out.visible = True.
    # But we cannot change visibility in return? We can use gr.update(visible=True) but that's tricky in output.
    # Simpler: just show the file output component all the time, but it will be empty initially.
    # When compute is clicked, it gets a file value; user can then click it to download.
    # That's acceptable. So we adjust: the file output is always visible (or initially hidden and we show via update).
    # We'll keep it visible; default no file.
    csv_file_out = gr.File(label="Download CSV (click to download)", visible=True)

    # update compute_btn click to include csv_file_out
    compute_btn.click(
        fn=run_horton,
        inputs=[f0, fc, k, t_start, t_end, dt],
        outputs=[table, plot, summary, csv_file_out]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
