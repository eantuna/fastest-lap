import fastest_lap
from fastest_lap import KMH
import csv
import numpy as np
import matplotlib.pyplot as plt
# print(plt.get_backend())

# Load vehicle
vehicle = "car"
fastest_lap.create_vehicle_from_xml(vehicle, "/mnt/e/Develop/Apex/fastest-lap/database/vehicles/f1/ferrari-2022-australia.xml")

# Load track
track = "catalunya"
fastest_lap.create_track_from_xml(track, "/mnt/e/Develop/Apex/fastest-lap/database/tracks/monaco/monaco.xml")
s = fastest_lap.track_download_data(track, "arclength")

# Compute optimal laptime
options  = "<options>"
options += "    <output_variables>"
options += "        <prefix>run/</prefix>"
options += "    </output_variables>"
options += "    <print_level> 5 </print_level>"
options += "</options>"
# fastest_lap.set_print_level(0)
prefix,variable_list = fastest_lap.optimal_laptime(vehicle, track, s, options)
run = fastest_lap.download_variables(prefix, variable_list)

x        = run["chassis.position.x"]
y        = run["chassis.position.y"]
delta    = run["front-axle.steering-angle"]
throttle = run["chassis.throttle"]
u        = run["chassis.velocity.x"]
s        = run["road.arclength"]
time     = run["time"]
psi      = run["chassis.attitude.yaw"]
omega    = run["chassis.omega.z"]
v        = run["chassis.velocity.y"]

# Transpose the dictionary (columns → rows)
rows = zip(*run.values())
with open('optimal_laptime_output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(run.keys())   # header
    writer.writerows(rows) 

# plt.plot(np.array(s), np.array(u)*2.237, color="orange")
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
ax1.plot(np.array(s), np.array(u)*2.237, color="orange")
ax1.set_ylabel("Velocity")
ax2.plot(np.array(s), np.array(throttle), color="red")
ax2.set_ylabel("Throttle")
ax3.plot(np.array(s), np.array(delta), color="red")
ax3.set_ylabel("Steering")
ax4.plot(np.array(s), np.array(psi), color="red")
ax4.set_ylabel("PSI")
ax4.set_xlabel("Distance")
x_center, y_center, x_left, y_left, x_right, y_right, theta = fastest_lap.track_coordinates(track)
ax5.plot(x_center,y_center,linewidth=0.5,color=(0.5372549019607843, 0.6039215686274509, 0.7215686274509804, 1.0),linestyle=(0, (20, 4)))
ax5.plot(x_left,y_left,linewidth=1,color=(0.5372549019607843, 0.6039215686274509, 0.7215686274509804, 1.0))
ax5.plot(x_right,y_right,linewidth=1,color=(0.5372549019607843, 0.6039215686274509, 0.7215686274509804, 1.0))
ax5.plot(x,y,linewidth=1,color="orange")
ax5.set_aspect(0.5)
ax5.invert_yaxis()
ax5.set_xticks([])
ax5.set_yticks([])
fig.suptitle("Optimal Lap Simulation")
plt.show()

fastest_lap.delete_variable("run/*")
print("Done")