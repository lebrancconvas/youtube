// clone the taskApp folder , cd into it, type make and run the exceutable ./main
#include <stdio.h>
#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#define maxItems 100
#define maxLength 50

typedef struct {
	char task[maxLength];
	int completed;
} todoItem;

typedef struct {
	todoItem items[maxItems];
	int count;

} todoList;

//saves to the file in the format of 0, Taskname 
//list->items[i].completed means in todolist items index i it'll return completed.
//list is a pointer which is referring to items of todoItem which has another two conditions
void saveToFile(todoList *list, const char *filename) {
	FILE *fp = fopen(filename, "w");
	if (fp != NULL) {
		for (int i = 0; i < list->count; i++) {
			fprintf(fp, "%d, %s\n", list->items[i].completed, list->items[i].task);
		}

	} else {
		perror("Error Opening file");
		return;
	}
	fclose(fp);
}
//just loads from a file while certain conditions are met, 2 is returned while is matches else it'll show error 
//so if it reads like 0, Taskname only then it'll show
void loadFromFile(todoList *list, const char *filename) {
	FILE *fp = fopen(filename, "r");
	if (fp != NULL) {
		list->count = 0;
		while (fscanf(fp, "%d, %[^\n]\n", &list->items[list->count].completed, list->items[list->count].task) == 2) {
			list->count ++;
			if (list->count >= maxItems) {
				break;
			}
		}
	} else {
		printf("Error opening file");
		return;
	}
}
//just adds items in list with count of list and task name default is 0 , so incomplete

void addItem(todoList *list, const char *task) {
	if (list->count >= maxItems) {
		printf("Max capacity reached, please complte previous tasks, you lazy bastard.");
		return;

	} else {
		strcpy(list->items[list->count].task, task);
		list->items[list->count].completed = 0;
		list->count++;
	}
}
//deletes an item when i is less than count minus 1 , so 4 items and it'll list 3 and return 3 instead of 4 so ++i
void deleteItem(todoList *list, int index) {
	if (index < 0 || index >= list->count) {
		printf("Invalid index\n");
		return;
	} else {
		for (int i = index; i < list->count - 1; ++i) {
			strcpy(list->items[i].task, list->items[i + 1].task);
			list->items[i].completed = list->items[i + 1].completed;
		}
		list->count--;
	}
}
//marking an object complete of the index of list items, so it turns 0 to 1 
void markComplete(todoList *list, int index) {
	if (index < 0 || index >= list->count) {
		printf("Invalid index.\n");
		return;
	} else {
		list->items[index].completed = 1;
	}
}
//print list for i wihint range of count.
void printList(todoList * list) {
	for (int i =  0; i < list->count; ++i) {
		printf("%d. [%c] %s\n", i + 1, (list->items[i].completed ? 'x' : ' '), list->items[i].task);
	}
}

int main() {
	todoList todolist;
	todolist.count = 0;

	initscr();
	cbreak();
	noecho();
	keypad(stdscr, TRUE);
	
	char fileName[] = "tasks.txt";
	loadFromFile(&todolist, fileName);

	int choice;
	char newTask[maxLength];

	do {
		clear();
		printw(":3-> Manage your tasks <-:3\n");
		printw(". . . . . . . . . . . . . . . . \n\n");
		for (int i = 0; i < todolist.count; ++i) {
			printw("%d. [%c] %s\n", i + 1, (todolist.items[i].completed ? 'x' : ' '), todolist.items[i].task);
		}
		printw("\n\n");
		printw("1-> Add new tasks.\n");
		printw("2-> Mark as completed.\n");
		printw("3-> Delete item.\n");
		printw("4-> Ssve and quit.\n");
		printw("\nEnter your choices pookie: ");
		refresh();

		echo();
		scanw("%d", &choice);
		refresh();


		switch (choice) {
			case 1:
				clear();
				printw("Add new task: ");
				refresh();
				echo();
				getstr(newTask);
				noecho();
				addItem(&todolist, newTask);
				break;
			case 2:
				clear();
				printw("Enter index of item to complete.");
				refresh();
				scanw("%d", &choice);
				noecho();
				markComplete(&todolist, choice - 1);
				break;
			case 3:
				clear();
				printw("Enter item index to be deleted: ");
				refresh();
				scanw("%d", &choice);
				deleteItem(&todolist, choice - 1);
				break;
			case 4:
				saveToFile(&todolist, fileName);
				break;
			default:
				printw("Invalid choice\n");
				break;
		}
		refresh();
		//while the choice is not 4 this will work, once we press 4 the loop will break
	} while (choice != 4);

	endwin();
	return 0;


}



















