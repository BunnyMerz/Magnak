def one_time_event(a,b,exceptions,expections_object,special_function,base_function):
    """
    for x in [a,b[
        where if x not in expections:
            base_function(x)
        else:
            special_function(expetions_objects[x])
    """
    exceptions.append(b)
    for x in range(a, exceptions[0]):
        base_function(x)
    for exp in range(len(exceptions) - 1):
        special_function(expections_object[exp])
        for x in range(exceptions[exp],exceptions[exp + 1]):
            base_function(x)