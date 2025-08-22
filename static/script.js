
const tasklist = document.getElementById("tasklist");
const form = document.getElementById("addNewTask");

tasklist.addEventListener("click", (event) => {
    // Check if the clicked element consist of delete in class list
if (event.target.classList.contains("delete")) {
    const myTaskDiv = event.target.closest(".task");
    const deleteID = myTaskDiv.id;

    if (deleteID) {
        fetch(`/tasks/delete/${parseInt(deleteID)-1}`, { method: "DELETE" })
            .then(response => response.json())
            .then(data => {
                if (data.message == "success") loadTask();
            });
        }
    }
if (event.target.classList.contains("status")){
    const myTaskDiv = event.target.closest(".task")
    const updateID = myTaskDiv.id;
    
    if (updateID){
        fetch(`/tasks/status/${parseInt(updateID)-1}`)
        .then(response=>response.json())
        .then(data =>{
            if(data.message=="success") loadTask();
        })
    }
}
})
function loadTask(){
    // This function call the api from the backend to load all the tasks 
        tasklist.innerHTML="";
    fetch("/get_tasks")
    .then(
        response => response.json())
    .then(data =>{
        data.forEach(element => {
            tasklist.innerHTML += `
            <div class="task" id="${parseInt(element.id)+1}">
                <div class="task-items">${parseInt(element.id)+1}</div>
                <div class="task-items" style="width: 45%;">${element.task_heading}</div>
                <div class="task-items status" style="width: 10%">${element.task_done}</div>
                <div class="task-items" style="width: 10%;">${element.task_due_date}</div>
                <div class="task-items delete" style="width: 10%;" id="delete">Delete Task</div>
            </div>`
        });
    });
}
//event listener for the submit action
form.addEventListener("submit",(event)=>{
    event.preventDefault();
    const formData = new FormData(form)
    console.log(formData);
    fetch("/add_task",{
        method:"POST",
        body:formData,
    }).then(response => response.json()).then(message =>{
        if(message.message=="success"){
            loadTask()
            form.reset()
        }
    })
})

//event listener to initially load the tasks
document.addEventListener("DOMContentLoaded",()=>{
    loadTask();
})