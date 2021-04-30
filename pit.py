def pitagoras(point1,point2):
    ## [(x0-x1)² + (y1-y0)²]^1/2
    points = [point1[0] - point2[0],point1[1] - point2[1]]
    distance = (points[0] ** 2 + points[1] ** 2)**(1/2)
    return distance
