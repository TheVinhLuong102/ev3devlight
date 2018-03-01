from os import listdir

def realrobot():
    """Check if program is being executed on an ev3dev device"""
    # Checking for a fixed file unique to ev3dev might be faster. 
    if 'lego-sensor' in listdir('/sys/class/'):
        return True
    else:
        return False

def read_int(infile):
    """Read an integer from a previously opened file descriptor"""
    infile.seek(0)    
    return(int(infile.read().decode().strip()))

def write_int(outfile, value):
    """Write an integer to a previously opened file descriptor"""
    outfile.write(str(int(value)))
    outfile.flush()

def read_str(infile):
    """Read a string from a previously opened file descriptor"""
    infile.seek(0)    
    return(infile.read().decode().strip())

def write_str(outfile, value):
    """Write a string to a previously opened file descriptor"""
    outfile.write(value)
    outfile.flush()

# Preconverted dutyvalue strings
duty_int2str = [str(i) for i in range(-100, 101)]

def write_duty(dutyfile, value):
    """ Like write_int, but 1 ms faster (which can be a factor 2 depending on your goal!).
    Suitable for quickly writing values with a known upper and lower bound
    """
    duty = max(min(100, int(value)), -100)  
    dutyfile.write(duty_int2str[duty+100])
    dutyfile.flush()  

def get_sensor_or_motor_path(device_type, port):
    """Get a path to a device based on port name. For example:
    
    get_device_path('tacho-motor', 'outA')

    For example, if port A is in the folder motor2, this returns the string

    /sys/class/tacho-motor/motor2
    
    """
    if realrobot():
        base_folder = '/sys/class/' + device_type
    else:
        base_folder = 'hardware/' + device_type

    # Iterate through list of numbered device folders (['motor0', 'motor1', 'motor2'] etc, or ['sensor0'] etc)
    for device_dir in listdir(base_folder):
        # In each folder, open the address file
        with open(base_folder + '/' + device_dir + '/address', 'r') as address_file:
            # Read the port string (e.g. 'outB')
            port_found = address_file.read().strip('\n')
            # If the port name matches, we are done searching and we know the full path
            if port in port_found:
                # Make the full path
                return base_folder + '/' + device_dir
    # Raise an error if the specified device is not attached
    raise Exception('Device not attached!')