// Función para obtener el token de la cookie
function getToken() {
    return document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
}

// Función para mostrar notificaciones
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerText = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Función para manejar la respuesta del dashboard
async function fetchDashboardData() {
    const token = getToken();
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const response = await fetch('/api/dashboard', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    if (!response.ok) throw new Error("Failed to fetch dashboard data");

    const data = await response.json();
    displayFiles(data.files); 
    return data;
}

// Cargar datos del dashboard al cargar el DOM
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await fetchDashboardData();
        displayFiles(data.files);
        displayUserInfo(data.name, data.role);
    } catch (error) {
        console.error("Error:", error);
    }

    // Event listeners
    document.getElementById('logoutButton')?.addEventListener('click', logout);
    document.getElementById('createUserButton')?.addEventListener('click', () => $('#createUserModal').modal('show'));
    document.getElementById('createTxtButton')?.addEventListener('click', () => $('#createTxtModal').modal('show'));
    document.getElementById('uploadTxtButton')?.addEventListener('click', () => $('#uploadTxtModal').modal('show'));
    document.getElementById('createUserForm')?.addEventListener('submit', createUser);
    document.getElementById('uploadFileButton')?.addEventListener('click', toggleFileOptions);
    document.getElementById('uploadTxtForm').addEventListener('submit', handleTxtUpload);
    document.getElementById('createTxtForm')?.addEventListener('submit', createTxtFile);
    document.getElementById('uploadImageForm').addEventListener('submit', handleImageUpload);
    document.getElementById('confirmDeleteButton').addEventListener('click', deleteConfirmedFile);
    document.getElementById('shareButton')?.addEventListener('click', () => openShareModal(fileId));
});

document.getElementById('myFilesLink').addEventListener('click', async () => {
    document.getElementById('sectionTitle').innerText = "Mis Archivos";
    const data = await fetchDashboardData();
    displayFiles(data.files, 'active');
});

function displayFiles(files, type = 'active') {
    const filesList = document.getElementById('filesList');
    filesList.innerHTML = files.map(file => {
        if (!file._id) {
            console.error("El archivo no tiene un _id:", file);
            return '';
        }

        const fileId = file._id.toString();
        const isImage = file.extension === 'png' || file.extension === 'jpg' || file.extension === 'jpeg';
        const iconPath = file.extension === 'txt' ? '/static/img/txt_icon.jpg' : `/static${file.directory}/${file.filename}`;

        let fileOptions = '';
        if (type === 'active') {
            fileOptions = `
                <button class="btn-icon share" onclick="openShareModal('${fileId}')" title="Compartir">
                    <i class="fas fa-share-alt"></i>
                </button>
                <button class="btn-icon delete" onclick="showDeleteConfirmation('${fileId}')" title="Eliminar">
                    <i class="fas fa-trash-alt"></i>
                </button>
                <button class="btn-icon view" onclick="viewFile('${fileId}')" title="Visualizar">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-icon edit" onclick="editFile('${fileId}')" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
            `;
        } else if (type === 'shared') {
            fileOptions = `
                <button class="btn-icon view" onclick="viewFile('${fileId}')" title="Visualizar">
                    <i class="fas fa-eye"></i>
                </button>
            `;
        } else if (type === 'thrashed') {
            fileOptions = `
                <button class="btn-icon restore" onclick="restoreFile('${fileId}')" title="Restaurar">
                    <i class="fas fa-undo"></i>
                </button>
                <button class="btn-icon delete" onclick="permanentlyDeleteFile('${fileId}')" title="Eliminar Permanentemente">
                    <i class="fas fa-trash-alt"></i>
                </button>
            `;
        }

        return `
            <div class="file-card">
                <div class="file-header">
                    <h3 class="file-name">${file.filename}</h3>
                    <button class="btn btn-secondary toggle-options" onclick="toggleOptions(this)">+</button>
                </div>
                <p class="file-description">${file.description || 'Sin descripción'}</p>
                <img src="${iconPath}" alt="${file.filename}" class="file-image">
                <p class="file-info">Extensión: ${file.extension}</p>
                <p class="file-owner">Subido por: ${file.owner}</p>
                
                <div class="file-options" style="display: none; text-align: center;">
                    ${fileOptions}
                </div>
            </div>
        `;
    }).join('');
}


async function viewFile(fileId) {
    try {
        const response = await fetch(`/api/files/${fileId}`, {
            headers: {
                'Authorization': 'Bearer ' + getToken()
            }
        });

        if (response.ok) {
            const fileData = await response.json();
            let contentHtml = `
                <p><strong>Autor:</strong> ${fileData.owner}</p>
                <p><strong>Descripción:</strong> ${fileData.description || 'Sin descripción'}</p>
            `;

            if (fileData.extension === 'txt') {
                contentHtml += `<pre>${fileData.content}</pre>`;
            } else if (['png', 'jpg', 'jpeg'].includes(fileData.extension)) {
                contentHtml += `<img src="/static${fileData.directory}/${fileData.filename}" alt="${fileData.filename}" class="img-fluid">`;
            }

            document.getElementById('filePreviewContent').innerHTML = contentHtml;
            const modal = new bootstrap.Modal(document.getElementById('filePreviewModal'));
            modal.show();
        } else {
            showNotification("Error al cargar la vista previa del archivo", "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showNotification("Error inesperado al cargar la vista previa", "error");
    }
}


function toggleOptions(button) {
    const options = button.closest('.file-card').querySelector('.file-options');
    options.style.display = options.style.display === 'none' ? 'block' : 'none';
}



// Función para mostrar el nombre del usuario y los botones según su rol
function displayUserInfo(name, role) {
    document.getElementById('userName').innerText = name || 'Usuario';
    const createUserButton = document.getElementById('createUserButton');
    createUserButton.style.display = (role === "Administrador") ? 'block' : 'none';
}

// Función para cerrar sesión
function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "/login";
}

// Función para enviar la solicitud de creación de usuario
async function createUser(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch('/api/create_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getToken()
            },
            body: JSON.stringify({ name, username, password, role })
        });

        if (response.ok) {
            showNotification("Usuario creado exitosamente");
            $('#createUserModal').modal('hide');
            document.getElementById('createUserForm').reset();
        } else {
            showNotification("Error al crear usuario", "error");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Función para alternar opciones de archivo
function toggleFileOptions() {
    const fileOptions = document.getElementById('fileOptions');
    fileOptions.style.display = fileOptions.style.display === 'none' ? 'block' : 'none';
}

async function createTxtFile(event) {
    event.preventDefault();
    const filename = document.getElementById('txtFilename').value;
    const description = document.getElementById('txtDescription').value;
    const content = document.getElementById('txtContent').value;

    try {
        const response = await fetch('/api/files/create_txt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getToken()
            },
            body: JSON.stringify({ filename, description, content })
        });

        if (response.ok) {
            showNotification("Archivo TXT creado exitosamente", "success");
            $('#createTxtModal').modal('hide');
            document.getElementById('createTxtForm').reset();

            const data = await fetchDashboardData(); 
            displayFiles(data.files);  
        } else {
            const result = await response.json();
            showNotification("Error al crear archivo: " + result.message, "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showNotification("Error inesperado al crear archivo", "error");
    }
}


document.getElementById('uploadImgButton')?.addEventListener('click', () => {
    $('#uploadImageModal').modal('show'); 
});

async function handleImageUpload(event) {
    event.preventDefault();
    const description = document.getElementById('imgDescription').value;
    const imageFile = document.getElementById('imgFile').files[0];

    const formData = new FormData();
    formData.append('description', description);
    formData.append('image', imageFile);

    try {
        const response = await fetch('/api/files/upload_image', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            body: formData
        });

        if (response.ok) {
            showNotification("Imagen subida exitosamente", "success");
            $('#uploadImageModal').modal('hide');
            document.getElementById('uploadImageForm').reset();

            const data = await fetchDashboardData(); 
            displayFiles(data.files); 
        } else {
            const result = await response.json();
            showNotification("Error al subir imagen: " + result.message, "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showNotification("Error inesperado al subir imagen", "error");
    }
}

//Func async para subir texto
async function handleTxtUpload(event) {
    event.preventDefault();
    const description = document.getElementById('txtDescription').value;
    const txtFile = document.getElementById('txtFile').files[0];

    if (!txtFile || txtFile.type !== "text/plain") {
        alert("Por favor, selecciona un archivo TXT válido.");
        return;
    }

    const formData = new FormData();
    formData.append('description', description);
    formData.append('file', txtFile);

    try {
        const response = await fetch('/api/files/upload_txt', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            },
            body: formData
        });

        if (response.ok) {
            showNotification("Archivo TXT subido exitosamente", "success");
            $('#uploadTxtModal').modal('hide');
            document.getElementById('uploadTxtForm').reset();

            const data = await fetchDashboardData();
            displayFiles(data.files);
        } else {
            showNotification("Error al subir archivo TXT", "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showNotification("Error inesperado al subir archivo TXT", "error");
    }
}

let fileIdToDelete = null;

function showDeleteConfirmation(fileId) {
    fileIdToDelete = fileId;
    const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    modal.show();
}

async function deleteConfirmedFile() {
    if (!fileIdToDelete) return;

    try {
        const response = await fetch(`/api/files/delete/${fileIdToDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + getToken()
            }
        });

        if (response.ok) {
            showNotification("Archivo movido a la papelera", "success");
            $('#deleteConfirmModal').modal('hide');
            const data = await fetchDashboardData();
            displayFiles(data.files);
        } else {
            showNotification("Error al mover el archivo a la papelera", "error");
        }
    } catch (error) {
        console.error("Error:", error);
        showNotification("Error inesperado al eliminar el archivo", "error");
    } finally {
        fileIdToDelete = null; 
    }
}

async function openShareModal(fileId) {
    console.log("Intentando obtener la lista de usuarios para compartir...");

    try {
        const response = await fetch('/api/users_list', {
            headers: {
                'Authorization': 'Bearer ' + getToken()
            }
        });

        if (response.ok) {
            const users = await response.json();
            console.log("Usuarios obtenidos:", users);
            const userList = document.getElementById('userList');
            userList.innerHTML = users.map(user => `
                <div>
                    <input type="checkbox" value="${user.username}" id="user_${user.username}">
                    <label for="user_${user.username}">${user.username}</label>
                </div>
            `).join('');
            window.fileToShare = fileId;
            const shareModal = new bootstrap.Modal(document.getElementById('shareModal'));
            shareModal.show();
        } else {
            showNotification("Error al obtener la lista de usuarios", "error");
        }
    } catch (error) {
        console.error("Error en openShareModal:", error);
        showNotification("Error inesperado al obtener la lista de usuarios", "error");
    }
}


window.shareFileWithUsers = async function () {
    const selectedUsers = Array.from(document.querySelectorAll('#userList input[type="checkbox"]:checked'))
        .map(checkbox => checkbox.value);

    if (selectedUsers.length === 0) {
        showNotification("Selecciona al menos un usuario para compartir el archivo", "warning");
        return;
    }

    try {
        const response = await fetch(`/api/files/share`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + getToken()
            },
            body: JSON.stringify({
                fileId: window.fileToShare,
                users: selectedUsers
            })
        });

        if (response.ok) {
            showNotification("Archivo compartido exitosamente", "success");
            $('#shareModal').modal('hide');
        } else {
            showNotification("Error al compartir el archivo", "error");
        }
    } catch (error) {
        console.error("Error al compartir el archivo:", error);
        showNotification("Error inesperado al compartir el archivo", "error");
    }
};

