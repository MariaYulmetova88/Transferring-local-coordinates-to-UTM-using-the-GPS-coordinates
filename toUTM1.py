import os.path
import math
import csv

#Read .csv file with local coordinates
def readFileIntoList(fileName,x1GPS,y1GPS):
    lst = []
    if os.path.isfile(fileName):
        file = open(fileName, "r")
        file.readline()
        for line in file:
            lst.append(line.replace(',', '.').strip().split(';'))
            lst[-1][0] = float(lst[-1][0]) + float(x1GPS)
            lst[-1][1] = float(lst[-1][1]) + float(y1GPS)

        file.close()
        return lst



'''
The formula for rotation:
x2rotated=x1+M*u
xnrotated=x1+M*un
, where M – rotation matrix, vector u – the vector from point1 to point2(UTM_original), vector un – the vector from point1 to pointn(UTM_original).
We can also write this formula:
Xn_rotated=x1+((xn(utm_original)-x1)*cosQ + (yn(utm_original)-y1)*sinQ)
yn_rotated=x1+ ( -(xn(utm_original)-x1)*sinQ + (yn(utm_original)-y1)*cosQ)

'''
def rotation(uTM1, cos, sin,x1GPS,y1GPS):
    lst=[]
    for row in range (0,len(uTM1)):
        lst.append([])
        xRotated=x1GPS+((float(uTM1[row][0])-x1GPS)*cos+(float(uTM1[row][-1])-y1GPS)*sin)
        yRotated=y1GPS+(-(float(uTM1[row][0])-x1GPS)*sin+(float(uTM1[row][-1])-y1GPS)*cos)
        lst[row].append(xRotated)
        lst[row].append(yRotated)
    return lst


x1GPS=eval(input("Please, enter the x GPS-coordinate of the point, which has coordinates (0,0) in the local system (for example, '564103.1410000')"))
y1GPS=eval(input("Please, enter the y GPS-coordinate of the point, which has coordinates (0,0) in the local system (for example, '5180459.7640000')"))
#csvFile=str(input("Please, enter the name (in quotes) of the csv file with local coordinates, for example, 'localCoord1.csv'"))
uTM1 = readFileIntoList("localCoord1.csv",x1GPS,y1GPS)
print(uTM1)




#To find the cos of an angle we need to know lengths of vectors and dot product. (cosQ= (u*v)/(||u||*||v||))
x2GPS=eval(input("Please, enter the x GPS-coordinate of the second point(for example, '564033.1460000')"))
y2GPS=eval(input("Please, enter the y GPS-coordinate of the second point(for example, '5180429.0290000')"))
vectorVx=x2GPS-x1GPS
print (vectorVx)
vectorVy=y2GPS-y1GPS
print(vectorVy)
lengthV=math.hypot(vectorVx, vectorVy)
print(lengthV)


x2GPSlocal=eval(input("Please, enter the x coordinate of the second point in the local coordinate system(for example, '-51.64')"))
y2GPSlocal=eval(input("Please, enter the y coordinate of the second point in the local coordinate system(for example,'-58.35')"))
x2GPSlocaltoUTM=x2GPSlocal+x1GPS
y2GPSlocaltoUTM=y2GPSlocal+y1GPS

vectorUx=x2GPSlocaltoUTM-x1GPS
print(vectorUx)
vectorUy=y2GPSlocaltoUTM-y1GPS
print(vectorUy)
lengthU=math.hypot(vectorUx,vectorUy)
print(lengthU)



dotProduct=vectorUx*vectorVx+vectorUy*vectorVy
print(dotProduct)

#Find the cos of the angle from the formula: cosQ= (u*v)/(||u||*||v||)
cos=dotProduct/(lengthU*lengthV)
print(cos)

#Find the sin of the angle from the formula: sin²Q+cos²Q=1
sin=math.sqrt(1-cos**2)
print(sin)



finalCoord= rotation(uTM1,cos,sin,x1GPS,y1GPS)
print(finalCoord)

#Write the data to .csv file
myFile = open('UTMcoordinates.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(finalCoord)

print("Writing complete")