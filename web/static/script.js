const url = "http://localhost:5000";
document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#peopleTable tbody");
    const jsonOutput = document.querySelector("#jsonOutput");
    const addForm = document.querySelector("#addForm");

    const updateUI = (data) => {
        tableBody.innerHTML = "";
        data.forEach(person => {
            const row = document.createElement("tr");
            row.dataset.id = person.id;  
            row.innerHTML = `
                <td><input type="text" value="${person.name}" class="edit-name" data-id="${person.id}"></td>
                <td>
                    <ul>
                        ${person.children.map(child => `<li>${child.name} <button class="remove-child" data-child-id="${child.id}" data-person-id="${person.id}">Remover</button></li>`).join('')}
                    </ul>
                    <input type="text" class="add-child" placeholder="Adicionar filho" data-person-id="${person.id}">
                    <button class="add-child-btn" data-person-id="${person.id}">Adicionar Filho</button>
                </td>
                <td>
                    <button class="edit-person" data-id="${person.id}">Editar</button>
                    <button class="delete-person" data-id="${person.id}">Excluir</button>
                </td>
            `;

            tableBody.appendChild(row);
        });

        data.forEach(obj => {
            // Remove a propriedade 'id' do objeto principal
            delete obj.id;
        
            // Para cada 'children', mantemos apenas o nome (primeiro item do array)
            obj.children = obj.children.map(child => child.name);
        });
          
        jsonOutput.textContent = JSON.stringify(data, null, 2);
    };

    const fetchData = async () => {
        const response = await fetch(`${url}/person`);
        const data = await response.json();
        updateUI(data);
    };

    addForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const name = document.querySelector("#name").value;
        //const children = document.querySelector("#children").value.split(",").map(child => child.trim());

        const responsePerson = await fetch(`${url}/person`, { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });

        if (responsePerson.ok) {
            const dataPerson = await responsePerson.json();
            const personId = dataPerson.person.id;

            for (const childName of children) {
                await fetch("/child", { 
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: childName, person_id: personId })
                });
            }
        }

        fetchData();
    });

    document.body.addEventListener("blur", async (event) => {
        if (event.target.classList.contains("edit-name")) {
            const personId = event.target.dataset.id;
            const newName = event.target.value;

            const response = await fetch(`${url}/person/${personId}`, { 
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: newName })
            });

            if (response.ok) {
                fetchData();
            }
        }
    }, true);

    document.body.addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete-person")) {
            const personId = event.target.dataset.id;

            const response = await fetch(`${url}/person/${personId}`, { 
                method: "DELETE"
            });

            if (response.ok) {
                fetchData();
            }
        }

        if (event.target.classList.contains("add-child-btn")) {
            const personId = event.target.dataset.personId;
            const childName = event.target.previousElementSibling.value;

            const responseChild = await fetch(`${url}/child`, { 
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: childName, person_id: personId })
            });

            if (responseChild.ok) {
                fetchData();
            }
        }

        if (event.target.classList.contains("remove-child")) {
            const childId = event.target.dataset.childId;
            const personId = event.target.dataset.personId;
            console.log(childId, personId);

            const responseChild = await fetch(`${url}/child/${childId}`, { 
                method: "DELETE"
            });

            if (responseChild.ok) {
                fetchData();
            }
        }
    });

    fetchData();
});
