namespace WordRoguelike.Core.Tests;

public class CoreInfoTests
{
    [Fact]
    public void Ping_ReturnsOk()
    {
        Assert.Equal("ok", CoreInfo.Ping());
    }
}
