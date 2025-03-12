xquery version "1.0";

module namespace cf = "http://example.com/custom-functions";

declare function cf:update-xbrl($filePath as xs:string, $nodePath as xs:string, $newValue as xs:string) as element()*
{
    let $xbrl := doc($filePath)  (: Load the XBRL file :)
    let $node := $xbrl/*/*[name() = $nodePath]  (: Find node by name :)

    return
        if (exists($node)) then
            <updated>{$node ! element {name()} {$newValue}}</updated>
        else
            <error>Node not found</error>
};