using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public class UIManager : MonoBehaviour
{
    public Dropdown objectDropdown;
    public Dropdown textureDropdown;
    public Button regenerateButton;
    private string[] textures = { "Metal", "Rocks", "Sandstone" };

    void Start()
    {
        textureDropdown.AddOptions(textures.ToList());
        RefreshObjectList();

        regenerateButton.onClick.AddListener(OnRegenerate);
        objectDropdown.onValueChanged.AddListener(OnObjectSelected);
        textureDropdown.onValueChanged.AddListener(OnTextureChanged);
    }

    void RefreshObjectList()
    {
        objectDropdown.ClearOptions();
        if (SceneGenerator.Instance == null) return;

        var names = SceneGenerator.Instance.createdObjects
            .Select((obj, i) => $"{i+1}: {obj.name}")
            .ToList();
        objectDropdown.AddOptions(names);
    }

    void OnRegenerate()
    {
        SceneGenerator.Instance.GenerateScene();
        RefreshObjectList();
    }

    void OnObjectSelected(int index)
    {
        Debug.Log($"Objeto seleccionado: {SceneGenerator.Instance.createdObjects[index].name}");
    }

    void OnTextureChanged(int textureIndex)
    {
        int objIndex = objectDropdown.value;
        if (objIndex >= SceneGenerator.Instance.createdObjects.Count) return;

        GameObject obj = SceneGenerator.Instance.createdObjects[objIndex];
        Renderer renderer = obj.GetComponent<Renderer>();

        Texture tex = Resources.Load<Texture>(textures[textureIndex]);
        if (tex != null)
        {
            renderer.material.mainTexture = tex;
        }
    }
}
