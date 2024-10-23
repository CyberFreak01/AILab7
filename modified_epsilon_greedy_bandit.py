import numpy as np

def modified_epsilon_greedy_bandit(time_steps):
    # Initialize parameters
    k = 10  # Number of arms
    epsilon = 0.1  # Exploration rate
    alpha = 0.1  # Step-size parameter (for non-stationary environment)

    q_true = np.zeros(k)  # True action values
    q_est = np.zeros(k)   # Estimated action values
    total_rewards = np.zeros(time_steps)  # Store rewards over time
    action_history = np.zeros(time_steps, dtype=int)  # Store action history

    for t in range(time_steps):
        # Update the true action values (random walk)
        q_true += np.random.normal(0, 0.01, k)

        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            # Exploration: Choose a random action
            action = np.random.randint(k)
        else:
            # Exploitation: Choose the action with the highest estimated reward
            action = np.argmax(q_est)

        # Reward received from the chosen action (random around true mean)
        reward = np.random.normal(q_true[action], 1)

        # Update the estimated value using the step-size parameter (α)
        q_est[action] += alpha * (reward - q_est[action])

        # Store the reward and action taken
        total_rewards[t] = reward
        action_history[t] = action

    return total_rewards, action_history

# Example usage
if __name__ == "__main__":
    time_steps = 1000
    rewards, actions = modified_epsilon_greedy_bandit(time_steps)
    print("Total Rewards:", rewards)
    print("Action History:", actions)
