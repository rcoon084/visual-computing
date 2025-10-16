using System;
using UnityEngine;
using System.Collections.Generic;

[Serializable]
public class ObjectData
{
    public string type;
    public Vector3 position;
    public Vector3 scale;
    public Color color;
    public string texture;
}

[Serializable]
public class ObjectList
{
    public ObjectData[] objects;
}

public class SceneGenerator : MonoBehaviour
{
    public static SceneGenerator Instance; 
    public List<GameObject> createdObjects = new List<GameObject>();
    private ObjectList data;

    void Awake()
    {
        Instance = this;
    }

    void Start()
    {
        GenerateScene();
    }

    public void GenerateScene()
    {
        foreach (var obj in createdObjects)
            Destroy(obj);
        createdObjects.Clear();

        TextAsset jsonFile = Resources.Load<TextAsset>("objects");
        data = JsonUtility.FromJson<ObjectList>(jsonFile.text);

        foreach (ObjectData obj in data.objects)
        {
            GameObject go = CreatePrimitive(obj);
            createdObjects.Add(go);
        }
    }

    GameObject CreatePrimitive(ObjectData obj)
    {
        GameObject go = null;

        switch (obj.type.ToLower())
        {
            case "cube": go = GameObject.CreatePrimitive(PrimitiveType.Cube); break;
            case "sphere": go = GameObject.CreatePrimitive(PrimitiveType.Sphere); break;
            case "cylinder": go = GameObject.CreatePrimitive(PrimitiveType.Cylinder); break;
            case "capsule": go = GameObject.CreatePrimitive(PrimitiveType.Capsule); break;
            default: return null;
        }

        go.transform.position = obj.position;
        go.transform.localScale = obj.scale;

        Renderer renderer = go.GetComponent<Renderer>();
        Material mat = new Material(Shader.Find("Standard"));

        if (!string.IsNullOrEmpty(obj.texture))
        {
            Texture tex = Resources.Load<Texture>($"textures/{obj.texture}");
            if (tex != null)
            {
                mat.mainTexture = tex;
                mat.color = Color.white;
            }
            else
            {
                Debug.LogWarning($"No se encontró la textura '{obj.texture}' en Resources.");
                mat.color = obj.color != default ? obj.color : Color.gray;
            }
        }
        else
        {
            mat.color = obj.color != default ? obj.color : Color.white;
        }

        renderer.material = mat;
        return go;
    }
}
