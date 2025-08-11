import { z } from 'zod';
export const bugfixInputSchema = z.object({
    file_content: z.string(),
    file_language: z.string(),
    bug_description: z.string()
});
export const bugfixOutputSchema = z.object({
    status: z.string(),
    fixed_code: z.string()
});
async function fixBugInCode(code_snippet, code_language, bug_description) {
  const payload = {
    code_snippet,
    code_language,
    bug_description
  };
    const response = await fetch('http://localhost:5000/fix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
        throw new Error(`API error : ${response.status} ${response.statusText}`);
    }

    return bugfixOutputSchema.parse(await response.json());
}
const userInput = {
  file_content: `
def hello():
    x = 5  # unused
    print("Hello, world!")
`,
  file_language: "Python",
  bug_description: "Remove unused variables"
};
async function main(){
    const args = bugfixInputSchema.parse(userInput);
    const result= await fixBugInCode(args.file_content,args.file_language,args.bug_description);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
}
main().then(res => console.log(res)).catch(err => console.error(err));
