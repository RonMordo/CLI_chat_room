import threading
import os
# def simple(x, y, z):
#     print(f"Answer = {x + y + z}.")

# if __name__=="__main__":

#     t1 = threading.Thread(target=simple, args=(2, 6, 7))
#     t2 = threading.Thread(target=simple, args=(1,2,3))

#     t1.start()
#     t2.start()

#     t1.join()
#     t2.join()

#     print("Done.")
#-----------------------------------------------------------------------------------------

# def task1():
# 	print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
# 	print("ID of process running task 1: {}".format(os.getpid()))

# def task2():
# 	print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
# 	print("ID of process running task 2: {}".format(os.getpid()))

# if __name__ == "__main__":

# 	print("ID of process running main program: {}".format(os.getpid()))

# 	print("Main thread name: {}".format(threading.current_thread().name))

# 	t1 = threading.Thread(target=task1, name='t1')
# 	t2 = threading.Thread(target=task2, name='t2')

# 	t1.start()
# 	t2.start()

# 	t1.join()
# 	t2.join()
#-----------------------------------------------------------------------------------------------

name = 'ron'
age = 12
print("His name is:{}, and his age is {}".format(name, age))
