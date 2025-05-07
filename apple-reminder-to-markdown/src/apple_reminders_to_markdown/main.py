#!/usr/bin/env python3

import os
import json
import typer

app = typer.Typer()

DEFAULT_REMINDERS_DIR = "reminders"
DEFAULT_OUTPUT_FILE = "reminders.md"

def generate_markdown_task(json_file_path) -> str:
    md_task = ""
    with open(json_file_path, "r") as json_file:
        task = json.load(json_file)

        # Generate the Markdown task
        source_list = task.get("List", "")
        state_tag = ""
        if source_list == "Next":
            state_tag = "#next"
        elif source_list == "Waiting":
            state_tag = "#waiting"
        elif source_list == "Someday":
            state_tag = "#someday"
        elif source_list == "Agendas":
            state_tag = "#discussion"
        elif source_list == "Read/Watch":
            state_tag = "#readwatch"

        is_completed = "x" if task.get("Is Completed", False) else " "
        title = task.get("Title", "Untitled")
        notes = task.get("Notes", "")

        other_tags = task.get("Tags", "")
        other_tags = other_tags.replace("P-", "#a/")

        due_date = task.get("Due Date", "")[:10]
        if due_date:
            due_date = f" 📅 {due_date}"

        completion_date = task.get("Completion Date", "")[:10]
        if completion_date:
            completion_date = f" ✅ {completion_date}"

        priority = task.get("Priority", "")
        if priority == "Low":
            priority = "⏬"
        elif priority == "High":
            priority = "🔺"
        elif priority == "None":
            priority = ""
        else:
            typer.echo(f"Unknown priority: {priority}")

        md_task = f"- [{is_completed}] {title} {state_tag} {other_tags} {priority}"
        if notes:
            notes = notes.replace("\n", "<br/>")
            md_task += f"<br/>{notes}"

        md_task += due_date
        md_task += completion_date

    return md_task


def process_reminders(reminders_dir: str, output_file: str):
    # Start the Markdown file
    with open(output_file, "w") as md_file:
        # Process each JSON file in the reminders directory
        for filename in os.listdir(reminders_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(reminders_dir, filename)
                md_task = generate_markdown_task(file_path)
                if md_task:
                    md_file.write(md_task + "\n")
    typer.echo(f"Processed {len(os.listdir(reminders_dir))} files.")
    typer.echo(f"Markdown file generated at {output_file}")
    # print(f"Markdown file generated at {output_file}")


@app.command()
def transform(
    reminders_dir: str = typer.Argument(DEFAULT_REMINDERS_DIR, help="Path to the reminders folder"),
    output_file: str = typer.Argument(DEFAULT_OUTPUT_FILE, help="Path to the output Markdown file")
):
    """
    Transform Apple Reminders JSON files into a Markdown file.
    """
    process_reminders(reminders_dir, output_file)

if __name__ == "__main__":
    app()
