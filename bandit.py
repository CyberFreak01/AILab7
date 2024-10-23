import numpy as np
import matplotlib.pyplot as plt

# Function to simulate rewards for a bandit action
def simulate_bandit(action):
    # Normally distributed rewards with mean = 0 and std dev = 0.01
    return np.random.normal(0, 0.01)

# Parameters
num_steps = 10000
cumulative_rewards = np.zeros((num_steps, 3))
individual_rewards = np.zeros((num_steps, 2, 3))
action_counts = np.zeros((10, 3))

epsilon_values = [0.01, 0.1, 0.3]

for idx, epsilon in enumerate(epsilon_values):
    step = 1
    while step <= num_steps:
        # Exploration phase
        if np.random.rand() < epsilon or step == 1:
            selected_action = np.random.randint(0, 10)  # Random action between 0 and 9
            reward = simulate_bandit(selected_action)
            cumulative_rewards[step - 1, idx] = reward
            if step > 1:
                cumulative_rewards[step - 1, idx] += cumulative_rewards[step - 2, idx]
            individual_rewards[step - 1, :, idx] = [reward, selected_action]

        # Exploitation phase
        else:
            action_stats = np.zeros((10, 2))  # To store total rewards and counts for actions
            for s in range(step - 1):
                action_stats[int(individual_rewards[s, 1, idx]), 0] += individual_rewards[s, 0, idx]  # Total rewards
                action_stats[int(individual_rewards[s, 1, idx]), 1] += 1  # Count of actions taken

            # Determine action with maximum expected return
            best_expected_return = -np.inf
            for action in range(10):
                if action_stats[action, 1] > 0:  # Avoid division by zero
                    expected_value = action_stats[action, 0] / action_stats[action, 1]
                    if expected_value > best_expected_return:
                        best_expected_return = expected_value
                        selected_action = action

            reward = simulate_bandit(selected_action)
            cumulative_rewards[step - 1, idx] = reward + cumulative_rewards[step - 2, idx]
            individual_rewards[step - 1, :, idx] = [reward, selected_action]
            action_counts[:, idx] = action_stats[:, 1]

        step += 1

# Calculate average rewards over time
average_reward = np.zeros(num_steps)
for i in range(num_steps):
    average_reward[i] = cumulative_rewards[i, 1] / (i + 1)

# Plotting average reward over time for epsilon = 0.1
plt.figure(figsize=(10, 6))
plt.plot(average_reward, label='Average Reward (epsilon = 0.1)')
plt.xlabel('Time Steps')
plt.ylabel('Average Reward')
plt.title('10-Armed Bandit Problem Simulation')
plt.legend()
plt.grid()
plt.show()

