using UnityEngine;

public class ControlCamaras : MonoBehaviour
{
    // Arrastra tus cámaras aquí en el Inspector de Unity
    public Camera camaraPerspectiva;
    public Camera camaraOrtografica;

    void Start()
    {
        // Nos aseguramos de empezar con la cámara perspectiva activada
        camaraPerspectiva.enabled = true;
        camaraOrtografica.enabled = false;
    }

    void Update()
    {
        // Revisa si se presionó la tecla 'C'
        if (Input.GetKeyDown(KeyCode.C))
        {
            // Invierte el estado 'enabled' de ambas cámaras
            camaraPerspectiva.enabled = !camaraPerspectiva.enabled;
            camaraOrtografica.enabled = !camaraOrtografica.enabled;
        }
    }
}
