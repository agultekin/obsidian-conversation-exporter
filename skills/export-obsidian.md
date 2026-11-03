# Skill: Export Obsidian

## Trigger
This instruction is triggered when the user inputs `/export-obsidian` or `/export-obsidian [subfolder]`.

## Behavior & Execution
1. Extract the full text and context of the current conversation session.
2. Determine the target directory inside the Obsidian vault:
   - Default root directory: `~/Obsidian/Vault/historic/`
   - If a subfolder argument is provided, save to `~/Obsidian/Vault/historic/[subfolder]/`.
3. Generate a concise, descriptive title based on the session topic.
4. Format the Markdown note using the filename structure `YYYY-MM-DD-title-slug.md` with standard YAML frontmatter (date, title, and tags).
5. Write the file to the target path and output a confirmation message to the user with the generated file path.
