#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ncurses.h>

#define MAX_ITEMS 100
#define MAX_LEN 50

struct TodoItem {
    char task[MAX_LEN];
    int completed;
};

struct TodoList {
    struct TodoItem items[MAX_ITEMS];
    int count;
};

void saveTodoList(struct TodoList *list, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        perror("Error opening file for writing");
        return;
    }
    
    for (int i = 0; i < list->count; ++i) {
        fprintf(fp, "%d,%s\n", list->items[i].completed, list->items[i].task);
    }
    
    fclose(fp);
}

void loadTodoList(struct TodoList *list, const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file for reading");
        return;
    }
    
    list->count = 0;
    while (fscanf(fp, "%d,%[^\n]\n", &list->items[list->count].completed, list->items[list->count].task) == 2) {
        list->count++;
        if (list->count >= MAX_ITEMS) {
            break;
        }
    }
    
    fclose(fp);
}

void addItem(struct TodoList *list, const char *task) {
    if (list->count >= MAX_ITEMS) {
        printf("Todo list is full, cannot add more items.\n");
        return;
    }
    
    strcpy(list->items[list->count].task, task);
    list->items[list->count].completed = 0;
    list->count++;
}

void removeItem(struct TodoList *list, int index) {
    if (index < 0 || index >= list->count) {
        printf("Invalid index.\n");
        return;
    }
    
    list->items[index].completed = 1;
}

void deleteItem(struct TodoList *list, int index) {
    if (index < 0 || index >= list->count) {
        printf("Invalid index.\n");
        return;
    }
    
    for (int i = index; i < list->count - 1; ++i) {
        strcpy(list->items[i].task, list->items[i + 1].task);
        list->items[i].completed = list->items[i + 1].completed;
    }
    
    list->count--;
}

void printTodoList(struct TodoList *list) {
    for (int i = 0; i < list->count; ++i) {
        printf("%d. [%c] %s\n", i + 1, (list->items[i].completed ? 'X' : ' '), list->items[i].task);
    }
}

int main() {
    struct TodoList todoList;
    todoList.count = 0;
    
    // Initialize ncurses
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    
    char filename[] = "todo.txt";
    loadTodoList(&todoList, filename);
    
    int choice;
    char newTask[MAX_LEN];
    
    do {
        clear();
        printw("TODO List:\n");
        printw("---------\n");
        for (int i = 0; i < todoList.count; ++i) {
            printw("%d. [%c] %s\n", i + 1, (todoList.items[i].completed ? 'X' : ' '), todoList.items[i].task);
        }
        printw("\n");
        printw("1. Add Item\n");
        printw("2. Mark Item as Completed\n");
        printw("3. Delete Item\n");
        printw("4. Save and Quit\n");
        printw("\nEnter your choice: ");
        refresh();
        
        scanw("%d", &choice);
        
        switch (choice) {
            case 1:
                clear();
                printw("Enter new task: ");
                refresh();
                echo();
                getstr(newTask);
                noecho();
                addItem(&todoList, newTask);
                break;
            case 2:
                clear();
                printw("Enter index to mark as completed: ");
                refresh();
                scanw("%d", &choice);
                removeItem(&todoList, choice - 1);
                break;
            case 3:
                clear();
                printw("Enter index to delete: ");
                refresh();
                scanw("%d", &choice);
                deleteItem(&todoList, choice - 1);
                break;
            case 4:
                saveTodoList(&todoList, filename);
                break;
            default:
                printw("Invalid choice.\n");
                break;
        }
        
        refresh();
    } while (choice != 4);
    
    endwin();
    
    return 0;
}























































































































































































































































































































