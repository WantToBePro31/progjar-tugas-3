from concurrent.futures import ThreadPoolExecutor
import time
import socket
import logging

def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.20.0.4', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        msg = 'TIME\r\n'
        logging.warning(f"sending {msg}")
        sock.sendall(msg.encode('utf-8'))
        # Look for the response
        data = sock.recv(32)
        result = data.decode('utf-8')
        logging.warning(f"{result}")
    finally:
        logging.warning("closing")
        sock.close()

if __name__=='__main__':
    with ThreadPoolExecutor() as ThreadPool:
        counter = 0
        max_thread_pool = 0
        request = set()
        start_time = time.time()
        while time.time() - start_time < 30:
            pool = ThreadPool.submit(send_data)
            request.add(pool)

            completed_request = {req for req in request if req.done()}
            request -= completed_request
            
            counter += len(completed_request)
            if counter > max_thread_pool:
                max_thread_pool = counter
                
        for req in request:
            req.result()
            
        f = open('maximum_threading_pool.txt', 'w')
        f.write(f"Maximum thread pools acquired: {max_thread_pool}")
        f.close
        
        logging.warning(f"Maximum thread pools: {max_thread_pool}")
    ThreadPool.shutdown(wait=True)