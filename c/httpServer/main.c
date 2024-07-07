#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <fcntl.h>


#define PORT 8000
#define MAXIMUM_REQUEST_SIZE 2048
#define ROOT "./src"

void handling(int sock) {
	//assigns an empty socket array of 0
	char request[MAXIMUM_REQUEST_SIZE] = {0};
	recv(sock, request, MAXIMUM_REQUEST_SIZE, 0); 
	
	// get/post ./src/index.html http/1.1 or 2
	char method[10], path[255], protocol[20];
	sscanf(request, "%s %s %s", method, path, protocol);
	
	char filePath[265];
	sprintf(filePath, "%s%s", ROOT, path);
	
	//if path = root / 
	if (strcmp(path, "/") == 0) {
		sprintf(filePath, "%s/index.html", ROOT);
	}

	if (strcmp(method, "GET") == 0) {
		int file = open(filePath, O_RDONLY);
		if (file == -1) { 
			char res[] = "HTTP/1.1 404 NOT FOUND\r\n\r\n";
			send(sock, res, strlen(res), 0);
		} else {
			char res[] = "HTTP/1.1 200 0K\r\n\r\n";
			send(sock, res, strlen(res), 0);
		
			char buf[1024];
			ssize_t readBytes; //returns error or true -1 = negative 0 means positive
		
			while ((readBytes = read(file, buf, sizeof(buf))) > 0) {
				send(sock, buf, readBytes, 0);
			}
			close(file);
		}
		close(sock);
	}
}

int main() {
	int serverSock, clientSock;
	struct sockaddr_in serverAddr, clientAddr;
	socklen_t lenAddr = sizeof(struct sockaddr_in);
	
	serverSock = socket(AF_INET, SOCK_STREAM, 0);
	if (serverSock == -1) {
		perror("Socket failed badly.");
		exit(EXIT_FAILURE);
	}

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_port = htons(PORT);

	if (bind(serverSock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1) {
		perror("Binding failed");
		exit(EXIT_FAILURE);
	}

	if (listen(serverSock, 10) < 0) {
		perror("Bad ear, listening failed.");
		exit(EXIT_FAILURE);
	}

	printf("Listening of port %d \n", PORT);

	while (1) {
		clientSock = accept(serverSock, (struct sockaddr *)&clientAddr, &lenAddr);
		if (clientSock < 0) {
			perror("Proposal decliend");
			exit(EXIT_FAILURE);
		}
		handling(clientSock);
	}
	return 0;
}


















