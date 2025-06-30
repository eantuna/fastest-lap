import fastest_lap

# Load vehicle
vehicle = "car"
fastest_lap.create_vehicle_from_xml(vehicle, "/mnt/e/Develop/Apex/fastest-lap/database/vehicles/f1/ferrari-2022-australia.xml")

# Load track
track = "catalunya"
fastest_lap.create_track_from_xml(track, "/mnt/e/Develop/Apex/fastest-lap/database/tracks/miami/miami.xml")
s=fastest_lap.track_download_data(track,"arclength");

# Compute optimal laptime
options  = "<options>"
options += "    <output_variables>"
options += "        <prefix>run_without_limits/</prefix>"
options += "        <variables>"
options += "            <chassis.throttle/>"
options += "            <chassis.velocity.x/>"
options += "            <road.arclength/>"
options += "            <integral_quantities.engine-energy/>"
options += "        </variables>"
options += "    </output_variables>"
options += "    <print_level> 5 </print_level>"
options += "</options>"

fastest_lap.optimal_laptime(vehicle,track,s,options)

u_wo             = fastest_lap.download_vector("run_without_limits/chassis.velocity.x")
throttle_wo      = fastest_lap.download_vector("run_without_limits/chassis.throttle")
s_wo             = fastest_lap.download_vector("run_without_limits/road.arclength")
engine_energy    = fastest_lap.download_scalar("run_without_limits/integral_quantities.engine-energy")
print(f'Engine energy used: {engine_energy:.3f}.')
print(f'Max speed: {max(u_wo):.3f}.')


# Compute optimal laptime (With Limits)
options  = "<options>"
options += "    <output_variables>"
options += "        <prefix>run/</prefix>"
options += "        <variables>"
options += "            <chassis.throttle/>"
options += "            <chassis.velocity.x/>"
options += "            <road.arclength/>"
options += "            <integral_quantities.engine-energy/>"
options += "        </variables>"
options += "    </output_variables>"
options += "    <integral_constraints>"
options += "        <engine-energy>"
options += "            <lower_bound> 0.0 </lower_bound>"
options += "            <upper_bound> 25.0 </upper_bound>"
options += "        </engine-energy>"
options += "    </integral_constraints> "
options += "    <print_level> 5 </print_level>"
options += "</options>"

fastest_lap.optimal_laptime(vehicle,track,s,options);

throttle      = fastest_lap.download_vector("run/chassis.throttle")
u             = fastest_lap.download_vector("run/chassis.velocity.x")
s             = fastest_lap.download_vector("run/road.arclength")
engine_energy = fastest_lap.download_scalar("run/integral_quantities.engine-energy")
print(f'Engine energy used: {engine_energy:.3f}.')
print(f'Max speed: {max(u):.3f}.')

import numpy as np
import matplotlib.pyplot as plt
# import mplcyberpunk

# plt.style.use("cyberpunk")
# plt.figure(figsize=(20,3))
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(s,np.maximum(0,throttle_wo), label='Throttle')
ax1.plot(s,np.maximum(0,throttle), label='Throttle With Limit')
ax2.plot(s,u_wo, label='Speed (KMH)')
ax2.plot(s,u, label='Speed With Limit(KMH)')

# mplcyberpunk.add_glow_effects()
ax1.legend()
ax2.legend()

plt.show()