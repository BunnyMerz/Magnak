def one_time_event(a,b,exceptions,exceptions_objects,special_function,base_function):
    """
    z = 0
    
    for x in [a,b[
        where if x not in expections:
            base_function(x)
        else:
            special_function(expetions_objects[z])
            z += 1
    """
    exceptions.append(b)
    # print(a,exceptions[:-1],exceptions[-1])
    for x in range(a, exceptions[0]):
        base_function(x)
    for exp in range(len(exceptions) - 1):
        special_function(exceptions_objects[exp])
        for x in range(exceptions[exp],exceptions[exp + 1]):
            base_function(x)