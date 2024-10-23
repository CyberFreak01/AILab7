import numpy as np
import matplotlib.pyplot as plt

# Number of actions (bandit arms)
num_actions = 10

# Initialize mean rewards for each action to zero
mean_rewards = np.zeros(num_actions)

# Function to simulate rewards from a non-stationary bandit, where mean rewards change over time
def simulate_nonstationary_bandit(action):
    global mean_rewards
    # Generate a reward from a normal distribution centered around the current mean with added noise
    return np.random.normal(mean_rewards[action], 1)

# Function to update the mean rewards with small random noise
def update_reward_means():
    global mean_rewards
    mean_rewards += np.random.normal(0, 0.01, num_actions)

# Parameters
num_steps = 10000
cumulative_rewards = np.zeros((num_steps, 3))
individual_rewards = np.zeros((num_steps, 2, 3))
action_counts = np.zeros((num_actions, 3))

epsilon_values = [0.01, 0.1, 0.3]

for index, epsilon in enumerate(epsilon_values):
    step = 1
    while step <= num_steps:
        # Update the mean rewards for all actions
        update_reward_means()

        # Exploration phase
        if np.random.rand() < epsilon or step == 1:
            selected_action = np.random.randint(0, num_actions)  # Choose a random action
            reward = simulate_nonstationary_bandit(selected_action)
            cumulative_rewards[step - 1, index] = reward
            if step > 1:
                cumulative_rewards[step - 1, index] += cumulative_rewards[step - 2, index]
            individual_rewards[step - 1, :, index] = [reward, selected_action]

        # Exploitation phase
        else:
            action_stats = np.zeros((num_actions, 2))  # Store total rewards and counts for actions
            for s in range(step - 1):
                action_stats[int(individual_rewards[s, 1, index]), 0] += individual_rewards[s, 0, index]  # Total rewards
                action_stats[int(individual_rewards[s, 1, index]), 1] += 1  # Count of actions taken

            # Determine the action with the highest expected reward
            best_expected_return = -np.inf
            for action in range(num_actions):
                if action_stats[action, 1] > 0:  # Avoid division by zero
                    expected_value = action_stats[action, 0] / action_stats[action, 1]
                    if expected_value > best_expected_return:
                        best_expected_return = expected_value
                        selected_action = action

            reward = simulate_nonstationary_bandit(selected_action)
            cumulative_rewards[step - 1, index] = reward + cumulative_rewards[step - 2, index]
            individual_rewards[step - 1, :, index] = [reward, selected_action]
            action_counts[:, index] = action_stats[:, 1]

        step += 1

# Calculate average rewards for epsilon = 0.1
average_reward = np.zeros(num_steps)
for i in range(num_steps):
    average_reward[i] = cumulative_rewards[i, 1] / (i + 1)

# Plotting average reward over time for epsilon = 0.1
plt.figure(figsize=(10, 6))
plt.plot(average_reward, label='Average Reward (epsilon = 0.1)')
plt.xlabel('Time Steps')
plt.ylabel('Average Reward')
plt.title('10-Armed Bandit Simulation (Non-Stationary)')
plt.legend()
plt.grid()
plt.show()
