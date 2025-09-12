using UnityEngine;

public class TransformController : MonoBehaviour
{
    [Header("Rotation")]
    public float rotationSpeed = 45f; // Degrees per second

    [Header("Scaling")]
    public float scaleFrequency = 1f; // Speed of the oscillation
    public float scaleAmplitude = 0.5f; // How much it grows and shrinks
    private Vector3 initialScale; // To store the original scale

    [Header("Smooth Random Translation")]
    public float movementDuration = 3f; // Time in seconds to move to a new point
    public float movementRadius = 5f; // Maximum distance for a new point
    private Vector3 targetPosition;
    private Vector3 startPosition;
    private float journeyTimer;

    void Start()
    {
        // Save the object's initial scale
        initialScale = transform.localScale;
        
        // Set the initial start position and pick the first random target
        startPosition = transform.position;
        PickNewTargetPosition();
    }

    void Update()
    {
        // --- 1. Constant Rotation  ---
        transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);

        // --- 2. Oscillating Scale  ---
        float scaleOscillation = 1.0f + Mathf.Sin(Time.time * scaleFrequency) * scaleAmplitude;
        transform.localScale = initialScale * scaleOscillation;

        // --- 3. Smooth Translation using Lerp ---
        // Increment our timer
        journeyTimer += Time.deltaTime;

        // Calculate the progress of our journey (a value from 0 to 1)
        float journeyProgress = Mathf.Clamp01(journeyTimer / movementDuration);

        // Use Vector3.Lerp to find the current position in the journey
        transform.position = Vector3.Lerp(startPosition, targetPosition, journeyProgress);

        // If the journey is complete, pick a new target and reset
        if (journeyProgress >= 1.0f)
        {
            startPosition = targetPosition; // The new start is where we just arrived
            PickNewTargetPosition(); // Pick a new destination
            journeyTimer = 0f; // Reset the timer
        }
    }

    void PickNewTargetPosition()
    {
        Vector2 randomPoint = Random.insideUnitCircle * movementRadius;
        targetPosition = new Vector3(randomPoint.x, randomPoint.y, transform.position.z);
    }
}