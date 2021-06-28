# Flask_Task_Api_with_Repl
todo api with Flask backend and python repl frontend


Problem Statement
·         Create a todo server that runs in the background, waiting for client calls.

·         Create a command-line REPL to manage a to-do list of tasks - which will call the todo server.


We will use 6 commands to enable this functionality:


add task - add a new task to the list.
update task - update the metadata of a specific task from the list.
complete task - update the status of the task to a completed state.
undo task - update the status of the task to an in-completed state.
delete task - remove the task from the list.
list tasks - list all tasks.
list completed tasks - list just the completed tasks.
 

·         You are free to choose the task data model, as long as it satisfies the commands above.

·         You need to handle failure cases (such as - completed a completed task? deleting a deleted task, and so on..)

·         You need to use some persistent layer, but you don’t need to persist data between runs - you can use in-memory DB (like h2).


Details
·         Our application will take in user input one line at a time.


Bold text denotes text that will be entered as-is, italics denote arguments that will be replaced by a value.

1. todo add-task "TASK NAME"

·         This command adds a new task to your list.

·         We cannot have tasks with the same name.

·         "TASK NAME" - STRING


2. todo update-task "TASK NAME" "NEW TASK NAME" 

·         This command updates a specific task in the list.

·         We cannot update a non-exist task.

·         We cannot update a completed task.

·         We cannot update a task to be completed/undo.

·         "TASK NAME" - STRING

·         "NEW TASK NAME" - STRING


3. todo complete-task "TASK NAME"

·         This command completes a specific task in the list (which means - updates the task state).

·         We cannot complete a non-exist task.

·         We cannot complete a completed task.

·         "TASK NAME" - STRING


4. todo undo-task "TASK NAME"

·         This command undo a specific task in the list (which means - updates the task state).

·         We cannot undo a non-exist task.

·         We cannot undo an in-completed task.

·         "TASK NAME" - STRING


5. todo delete-task "TASK NAME"

·         This command deletes a specific task from the list.

·         We cannot delete a non-exist task.

·         "TASK NAME" - STRING


6. todo list-tasks

·         List all tasks.


7. todo list-completed-tasks

·         List completed tasks only.

