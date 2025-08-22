from flask import Flask , jsonify , request , render_template

class Task:
    '''This class provides the bluprint of a task'''
    def __init__(self,task_heading:str,task_due_date, task_done=False):
        self.id = None
        self.task_heading = task_heading.lower().capitalize()
        self.task_done = "Done" if task_done else "Pending",
        self.task_due_date = task_due_date if task_due_date else "Not set"
    def get_dict(self):
        '''this function return the dict version of the instance of the class for jsonify to sent to frontend'''
        return{
            "id":self.id,
            "task_heading":self.task_heading,
            "task_done": self.task_done,
            "task_due_date": self.task_due_date
        }
    
class TaskBook:
    '''This class aims to handle the list of tasks and provides function of adding , removing and showing the tasks'''
    def __init__(self):
        self.tasks = []

    def add_task(self,task:Task):
        '''Add new task to the list in form of dict '''
        task.id = len(self.tasks)
        taskdict = task.get_dict()
        self.tasks.append(taskdict)
         
    def remove_task(self,task_id:int):
        found = False
        try:
            for i , task in enumerate(self.tasks):
                if (task.get("id")) == int(task_id):
                    self.tasks.pop(i)
                    found = True
                    break
            #updating the task id after deleting
            for i,task in enumerate(self.tasks):
                task["id"] = i
            if found:
                print("Task deleted successfully")
        except Exception as e:
            print(e)
            print("Task not found")

    def get_tasks(self):
        '''To return the task List'''
        return self.tasks
    
    def toggle_task(self,task_id:int):
        print("Trying to toggle the task status")
        if  task_id <len(self.tasks) and 0<=task_id:
            for i , task in enumerate(self.tasks):
                print(task.get("task_due_date"))
                if(task.get("id")==int(task_id)):
                    if (task.get("task_done")=="Done"):
                        task["task_done"] = "Pending"
                    else:
                        task["task_done"] = "Done"
        else:
            print("\n Please enter the valid task id")


app = Flask("__main__")
taskbook = TaskBook()


@app.route('/add_task',methods=['POST'])
def taskAdder():
    task_heading = request.form.get("task_heading")
    task_due_date = str(request.form.get("task_due_date"))
    newTask = Task(task_heading,task_due_date,False)
    taskbook.add_task(newTask)
    return jsonify({"message":"success"})

@app.route('/tasks/delete/<int:task_id>',methods=['DELETE'])
def taskRemover(task_id:int):
    '''This function asks the user the task id to remove and tries to remove it from the taskbook'''
    taskbook.remove_task(task_id)
    return jsonify({"message":"success"})

@app.route('/tasks/status/<int:task_id>')
def toggleTask(task_id:int):
    taskbook.toggle_task(task_id)
    return jsonify({"message":"success"})

@app.route('/')
def home():
    return render_template("./index.html")

@app.route('/get_tasks' , methods = ['GET'])
def getTask():
    tasks = taskbook.get_tasks()
    return jsonify(tasks)

if __name__ == "__main__":
    taskbook.add_task(Task("Hello",False,None))
    taskbook.add_task(Task("Bye",False,None))
    taskbook.add_task(Task("AWW",False,None))
    app.run()