using UnityEngine;

public class OrbitCamera : MonoBehaviour
{
    public float sensitivity = 2f;
    private float rotationX = 0f;
    private float rotationY = 0f;

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    void Update()
    {
        float mouseX = Input.GetAxis("Mouse X") * sensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * sensitivity;

        rotationX += mouseX;
        rotationY -= mouseY;

        rotationY = Mathf.Clamp(rotationY, -90f, 90f);

        // Aplicar rotación a la cámara
        transform.localRotation = Quaternion.Euler(rotationY, rotationX, 0f);
    }
}
