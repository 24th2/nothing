import socket
import time
import sys

# Configuration settings - change these values as needed
DEFAULT_SETTINGS = {
    "server_ip": "paradisbox.pikamc.vn",
    "server_port": 25532,
    "packet_size": 1000000,
    "interval": 0.0  # Set to 0 for maximum speed
}

class MinecraftTCPSender:
    def __init__(self, server_ip, server_port, packet_size, interval):
        self.server_ip = server_ip
        self.server_port = server_port
        self.packet_size = packet_size
        self.interval = interval
        self.is_sending = False
        self.socket = None
        self.packet_count = 0
        self.start_time = None
        
    def connect(self):
        """Establish a TCP connection to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5-second timeout for connection
            print(f"Connecting to {self.server_ip}:{self.server_port}...")
            self.socket.connect((self.server_ip, self.server_port))
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def start_sending(self):
        """Start sending packets"""
        if not self.connect():
            return False
            
        self.is_sending = True
        self.packet_count = 0
        self.start_time = time.time()
        
        # Create a packet with null bytes
        packet_data = b'\x00' * self.packet_size
        
        print(f"Starting to send {self.packet_size} byte packets")
        if self.interval > 0:
            print(f"Interval: {self.interval} seconds")
        else:
            print("Sending at maximum speed (no delay)")
        print("Press Ctrl+C to stop...")
        
        try:
            while self.is_sending:
                try:
                    # Send the packet
                    self.socket.send(packet_data)
                    self.packet_count += 1
                    
                    # Display stats for every packet
                    elapsed_time = time.time() - self.start_time
                    packets_per_sec = self.packet_count / elapsed_time
                    total_data_sent = self.packet_count * self.packet_size
                    print(f"Packet {self.packet_count}: {total_data_sent} bytes total, {packets_per_sec:.2f} packets/sec")
                    
                    # Wait for the next packet if interval > 0
                    if self.interval > 0:
                        time.sleep(self.interval)
                        
                except Exception as e:
                    print(f"Error sending packet: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\nStopping packet sender...")
        
        self.stop_sending()
        return True
    
    def stop_sending(self):
        """Stop sending packets and close connection"""
        self.is_sending = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        # Display final statistics
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            packets_per_sec = self.packet_count / elapsed_time if elapsed_time > 0 else 0
            total_data_sent = self.packet_count * self.packet_size
            
            print(f"\nFinal statistics:")
            print(f"Total packets sent: {self.packet_count}")
            print(f"Total data sent: {total_data_sent} bytes")
            print(f"Duration: {elapsed_time:.2f} seconds")
            print(f"Average rate: {packets_per_sec:.2f} packets/sec")

def get_input(prompt, default=None, input_type=str):
    """Helper function to get user input with optional default value"""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if user_input == "":
                    return input_type(default)
                return input_type(user_input)
            else:
                user_input = input(f"{prompt}: ").strip()
                if user_input == "":
                    print("This field is required. Please enter a value.")
                    continue
                return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            sys.exit(0)

def main():
    print("Minecraft TCP Packet Sender")
    print("=" * 30)
    
    # Use default settings but allow customization
    print("Current default settings:")
    print(f"  Server: {DEFAULT_SETTINGS['server_ip']}:{DEFAULT_SETTINGS['server_port']}")
    print(f"  Packet size: {DEFAULT_SETTINGS['packet_size']} bytes")
    print(f"  Interval: {DEFAULT_SETTINGS['interval']} seconds")
    print("\nPress Enter to use defaults or enter new values:")
    
    # Get user input with defaults
    server_ip = get_input("Server IP", DEFAULT_SETTINGS["server_ip"])
    server_port = get_input("Server port", DEFAULT_SETTINGS["server_port"], int)
    packet_size = get_input("Packet size (bytes)", DEFAULT_SETTINGS["packet_size"], int)
    interval = get_input("Interval between packets (seconds)", DEFAULT_SETTINGS["interval"], float)
    
    # Validate inputs
    if packet_size <= 0:
        print("Error: Packet size must be positive")
        return
    
    if interval < 0:
        print("Error: Interval cannot be negative")
        return
    
    # Create and start the sender
    sender = MinecraftTCPSender(server_ip, server_port, packet_size, interval)
    sender.start_sending()

if __name__ == "__main__":
    main()