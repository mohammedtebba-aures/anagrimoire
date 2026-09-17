namespace WordRoguelike.Core;

/// <summary>
/// Placeholder surface so the Godot project can call into Core before rules exist.
/// </summary>
public static class CoreInfo
{
    /// <summary>
    /// Returns a constant token proving Core is loaded.
    /// </summary>
    public static string Ping() => "ok";
}
