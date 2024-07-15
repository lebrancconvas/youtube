#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PORT 8080
#define MAX_BUFF_SIZE 1024

void send_file(int client_socket, const char *filename, const char *content_type) {
    char response[MAX_BUFF_SIZE];
    char file_buffer[MAX_BUFF_SIZE];
    int file_fd, bytes_read;

    // Open html and css
    file_fd = open(filename, O_RDONLY);
    if (file_fd == -1) {
        perror("Failed to open file");
        exit(EXIT_FAILURE);
    }

    // Sending http response
    snprintf(response, sizeof(response),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: %s\r\n\r\n", content_type);

    write(client_socket, response, strlen(response));

    // Send html data, the logic is to loop through every buffer until the bytes read value is not 0, so eof
    while ((bytes_read = read(file_fd, file_buffer, sizeof(file_buffer))) > 0) {
        write(client_socket, file_buffer, bytes_read);
    }

    close(file_fd);
}

void handle_connection(int client_socket) {
    char request[MAX_BUFF_SIZE];
    char method[MAX_BUFF_SIZE];
    char path[MAX_BUFF_SIZE];
    char *query;
    char *input_value = NULL;
    char response[MAX_BUFF_SIZE];

    // Sending client request
    read(client_socket, request, sizeof(request));

    sscanf(request, "%s %s", method, path);

    // Send the client html and css 
    if (strcmp(path, "/") == 0 || strstr(path, "/index.html") != NULL) {
        send_file(client_socket, "index.html", "text/html");
    } else if (strstr(path, "/style.css") != NULL) {
        send_file(client_socket, "style.css", "text/css");
    } else {
        // Return 404 Not Found for any other requests
        char response[] = "HTTP/1.1 404 Not Found\r\n\r\n";
        write(client_socket, response, strlen(response));
        close(client_socket);
        return;
    }

    // Take input value 
    query = strchr(request, '?');
    if (query != NULL) {
        // Get input value
        input_value = strstr(query, "input=");
        if (input_value != NULL) {
            input_value += strlen("input=");
            char *end_of_value = strchr(input_value, '&');
            if (end_of_value != NULL) {
                *end_of_value = '\0';
            }

            // It's returning everything and not just the typed input :sob:
            snprintf(response, sizeof(response),
                     "<p>You entered: %s</p>\r\n", input_value);
            write(client_socket, response, strlen(response));
        }
    }
    close(client_socket);
}

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_length = sizeof(client_address);

    // Creating the socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Idek what this does, copied from stackoverflow but it works
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);

    // Binding
    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server is running on port %d...\n", PORT);

    // It's gonna take only one connection , no threading
    while (1) {
        client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_address_length);
        if (client_socket < 0) {
            perror("Accept failed");
            exit(EXIT_FAILURE);
        }

        // Call the server to handle this shit 
        handle_connection(client_socket);
    }

    return 0;
}





































































































































