// Función para obtener el token de autenticación desde las cookies
function getToken() {
    return document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
}

// Función para obtener y mostrar los archivos compartidos
async function fetchAndDisplaySharedFiles() {
    try {
        const token = getToken();
        console.log("Token obtenido:", token);

        const response = await fetch('/files/shared_test', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        });

        if (!response.ok) throw new Error("Error al cargar archivos compartidos");

        const files = await response.json();
        displaySharedFiles(files);
    } catch (error) {
        console.error("Error al cargar archivos compartidos:", error);
        showNotification("Error inesperado al cargar archivos compartidos", "error");
    }
}


// Función para mostrar los archivos compartidos en la página
function displaySharedFiles(files) {
    const filesList = document.getElementById('sharedFilesList');
    filesList.innerHTML = files.map(file => {
        const fileId = file._id;
        const isImage = file.extension === 'png' || file.extension === 'jpg' || file.extension === 'jpeg';
        const iconPath = isImage ? `/static${file.directory}/${file.filename}` : '/static/img/txt_icon.jpg';

        return `
            <div class="file-card">
                <div class="file-header">
                    <h3 class="file-name">${file.filename}</h3>
                </div>
                <p class="file-description">${file.description || 'Sin descripción'}</p>
                <img src="${iconPath}" alt="${file.filename}" class="file-image">
                <p class="file-info">Extensión: ${file.extension}</p>
                <p class="file-owner">Subido por: ${file.owner}</p>
            </div>
        `;
    }).join('');
}

// Mostrar una notificación en la página
function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.className = `alert alert-${type}`;
    document.getElementById('notificationMessage').textContent = message;
    notification.style.display = 'block';
    setTimeout(() => notification.style.display = 'none', 3000);
}

// Llamar a la función para cargar archivos compartidos cuando se cargue la página
document.addEventListener('DOMContentLoaded', fetchAndDisplaySharedFiles);
